subroutine lower_case(word)
  ! convert a word to lower case
  character (len=*) , intent(in out) :: word
  integer                            :: i,ic,nlen
  nlen = len(word)
  do i=1,nlen
     ic = ichar(word(i:i))
     if (ic >= 65 .and. ic < 90) word(i:i) = char(ic+32)
  end do
end subroutine lower_case


