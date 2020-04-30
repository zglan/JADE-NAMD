
    subroutine sub_fragit ( n_state, n_atom, n_block, n_col)
      !
      ! read in fort.52 and dump state_*.dat
      !
      implicit none
      integer :: n_state, n_atom, n_block, n_col
      double precision, allocatable, dimension(:,:,:,:) :: total
      double precision, allocatable, dimension(:,:,:) :: fin
      integer, allocatable, dimension(:,:) :: block_atom 
      integer, allocatable, dimension(:) :: atom_number
      character(len=2) :: outname
                             
      integer :: i, j, k, l, m, state, atom, column, block, tmp

      ! remove gs state
      state = n_state - 1
      atom = n_atom
      column = n_col
      block = n_block
      
      allocate (block_atom(block,atom)) 
      allocate (total(state,atom,atom,column))
      allocate (fin(state,block,block))

      open(unit=11, file="fort.52")

      do i=1,state
         do j=1,atom
            do k=1,atom
               read (11,*) total(i,j,k,:)
            enddo
         enddo
      enddo
   
      close(11)

      do i=1,block
         do j=1,atom
            block_atom(i,j)=0
         enddo
      enddo

      open(unit=12, file="block.in")

      do i=1,block
         read (12,*) tmp
         allocate (atom_number(tmp))
         read (12,*) (atom_number(j), j=1,tmp)
         do j=1,tmp
            block_atom(i,atom_number(j))=1
         enddo
         deallocate(atom_number)
      enddo

      
      close(12)
    
      do i=1,state
         do j=1,block
            do k=1,block
               fin(i,j,k)=0.d0
               do l=1,atom
                  do m=1,atom
                     fin(i,j,k)=fin(i,j,k) &
                                +total(i,l,m,3) &
                                *block_atom(j,l) &
                                *block_atom(k,m)
                  enddo
               enddo
            enddo
         enddo
      enddo

!      do i=1,state
!         do j=1,block
!            do l=1,column
!               fin(i,j,l)=0.d0
!               do k=1,atom
!                  fin(i,j,l)=fin(i,j,l)+block_atom(j,k)*total(i,k,l)
!               enddo
!            enddo
!         enddo
!      enddo
               
      do i=1,state
         write(outname,'(i2)') i
         open(unit=13, file='state_'//trim(adjustl(outname))//'.dat')
         do j=1,block
            do k=1,block
               write(13,'(f13.8)',advance="no") fin(i,j,k)
            enddo
               write(13,*)
         enddo
         close(13)
      enddo

      deallocate (total)
      deallocate (fin)
    end subroutine sub_fragit


!program main
!  call sub_fragit(20, 38, 12, 3)
!end
