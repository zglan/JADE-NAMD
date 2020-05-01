!ca**********************************************************************
!c readln
!c**********************************************************************
!c
      subroutine readln(string,word,nword,isec,ieof,iscend)
!c
!c     Created:  Feb 22. 2004 by Hai Lin
!c
!c     This subroutine finds the first non-comment and non-blank line
!c     from the input file (iunit), 
!c     where each line has at most 80 characters,
!c     and chop the line into words according to the space locations.
!c
!c     It returns the number of the words in (nword), and the individual 
!c     word in array (word) after changing to upper case.
!c
!c     The flags are also set 
!c        if it is beginning of a section (isec), 
!c     or if it is end of the file (ieof)
!c     or if it is end of the section (iscend).
!c
      implicit none
!c
!c  i/o variables
!c
      integer  nword
      integer  ieof, isec, iscend
      character*80  word(40)
      character*80  string
!c            
!c  local variables
!c
      integer  ip, icom, ibeg      
      character*81  line, sename, upcse
!c
      isec = 0
      ieof = 0
      iscend = 0
      nword = 0
!c
!c10    read(iunit,'(a80)',end=500) string

10    continue

!c      
      ip = 0
!c
!c     find the first nonblank character in a line
!c
20    ip = ip + 1
      if (string(ip:ip) .eq. ' ' .and. ip .le. 80) goto 20           
!c
!c     if it all blank or it is a comment line then read the next line
!c
      if (ip .gt. 80 .or. string(ip:ip) .eq. '#')  goto 10
!c
!c     convert to uppercase
!c
      line = upcse(string)
!C
!C     Find the position of a comment character, if any,
!C     in a nonblank noncomment line
!C
      icom = ip 
50    icom = icom + 1
      if (line(icom:icom) .ne. '#' .and. icom .le. 80)  goto 50         

55    if (ip .lt. icom) then
         ibeg = ip
60       ip = ip + 1
         if (line(ip:ip) .ne. ' ' .and. ip .lt. icom) goto 60 
         nword = nword + 1
         word(nword) = line(ibeg:ip-1)
70       ip = ip + 1
         if (line(ip:ip) .eq. ' ' .and. ip .lt. icom) goto 70
         goto 55
      endif
!c
!c     find the section name
!c
      if (word(1)(1:1) .eq. '*') then
         sename = word(1)(2:)
         word(1) = sename
         isec = 1
      endif
!c
!c
!c     find if section ends
!c
      if (word(1)(1:3) .eq. 'END') then
         iscend = 1
      endif
      return

500   ieof = 1

      return

      end


c***************************************************************************
c upcse 
c***************************************************************************
c
      function upcse(string)
c      
c     Purpose:  consistent case
c     
c     Created:  Feb. 22, 2004 by Hai Lin
c
c     Revised:
c
c     Description:  this function takes a string of 80 characters and
c                   converts all the lower case letters to upper case.
c
c     Called by: 
c     Calls:
C   Function which takes a string of 80 characters and converts the 
C   lower case letters in the string to upper case letters
C   This functions is a modified version of CASE which was written
C   by Rozeanne Steckler
C
      implicit none 
c
c  i/o variables
c
      character*80 string, upcse
c      
c  local variables
c
      integer  itry, i
      character*80 line
      character * 1 xlett
c
      line = string
      do 10 i = 1, 80
         xlett = line(i:i)
         itry = ichar (xlett)
         if (xlett .ge. 'a' .and. xlett .le. 'z') then 
            itry = itry - 32
            line(i:i) = char (itry)
         endif
10    continue
c
      upcse  = line 
c
      return
c
      end
c
c
c*******************************************************************************
c  ICINT
c*******************************************************************************
c
      function icint(svalue)
c
c     Created:  April 20, 1999 by P. L. Fast
c     Revised:
c     Purpose:  Convert a string into an integer
c
c     Called by:  rmlgen,rmlopt,
c     Calls:  fchar, fspace
c
c      use files, only : outfile
      implicit none
c
      integer icint, ibeg, ifin, iblnk, ierr, length, isign
      integer istart, i, n
      character*(*) svalue
      character ch
      length = len(svalue)
      if (length .eq. 0) then
         icint = 0
         return
      endif
c
c     find the first nonblank character
c
      ibeg = 1
      call fchar(svalue, ibeg, iblnk)
c
c     if it is a blank string set function to zero
c    
      if (iblnk .eq. 1) then
         icint = 0
         return
      endif
c
c     find the first blank character after the number
c
      ifin = ibeg+1
      call fspace(svalue, ifin, ierr)
      if (ierr .eq. 1) then
         ifin = length
      else
         ifin = ifin - 1
      endif
c
c     strip the blanks before and after the number
c
      svalue = svalue(ibeg:ifin)
      length = ifin - ibeg + 1
c
c
c     check for negative or positive sign (- or +)
c
      icint = 0
      istart = 2
      isign = +1
      if (svalue(1:1).eq.'+') then
         isign = +1
         ibeg = ibeg + 1
      elseif (svalue(1:1).eq.'-') then
         isign = -1
         ibeg = ibeg + 1
      else
         istart = 1
      endif
c
c     now convert each character to an integer - and store in icint
c
      do 70 i = ibeg,length
         ch = svalue(i:i)
         if (ch .ge. '0' .and. ch .le. '9') then
            n = ichar(ch) - ichar('0')
            icint = icint * 10 + n
         else
c            write(outfile,1000) svalue
            stop 'icint 1'
         endif
70    continue
      icint = icint * isign
c
      return
1000  format(/3x,'ERROR: illegal digit in an integer: ',A80)
      end
c  
c*******************************************************************************
c  FCHAR
c*******************************************************************************
c  
      subroutine fchar(string, istrt, ierr)
c               
c     Created:  June 18, 1999 by J. M. Rodgers
c     Revised:
c     Purpose:  Find the next character on the line
c
c     Description:  Scrolls through the positions in string starting
c         at position istrt.  Sets istrt to position of first character.
c         If there is no character left on the line, sets ierr to 1.
c
c     Called by:  rline, rlist, rword, cfloat, icint, rcoef
c     Calls:
c
      implicit none
c
      integer istrt, ierr, char, length
      character*(*) string
      ierr = 0
      char = 0
      length = len(string)
      do while (istrt .le. length .and. char .eq. 0)
         if (string(istrt:istrt) .ne. ' ') then
            char = 1
         elseif (istrt .eq. length) then
            ierr = 1
         endif
         istrt = istrt + 1
      enddo
c
c     Sets istrt back 1 in order to counteract increment at end
c       of do-while loop.
c
      istrt = istrt -1
      return
      end

c
c
c*******************************************************************************
c  FSPACE
c*******************************************************************************
c
      subroutine fspace(string, istrt, ierr)
c
c     Created:  June 18, 1999 by J. M. Rodgers
c     Revised:
c     Purpose:  Find the next space on the line
c
c     Description:  Scrolls through the positions in string starting
c        at position istrt.  Sets istrt to the position of the first
c        space.  Or if there is no spacebar left on the line, sets
c        ierr to 1.
c
c     Called by:  rword, cfloat, icint, rvar, rcoef
c     Calls:
c
      implicit none
c
      integer istrt, ierr, blnk, length
      character*(*) string
      ierr=0
      blnk = 0
      length = len(string)
      do while (istrt .le. length .and. blnk .eq. 0)
         if (string(istrt:istrt) .eq. ' ') then
            blnk = 1
         elseif (istrt .eq. length) then
            ierr = 1
         endif
         istrt = istrt + 1
      enddo
c
c     Sets istrt back 1 in order to counter act increment at end
c       of do while loop.
c
      istrt = istrt - 1
      return
      end



