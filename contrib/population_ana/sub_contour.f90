    subroutine sub_contour (n_state, n_bin, n_row, n_col)
      !
      ! build counter figure
      !
      ! read in state_*.dat and dump state_mod_*.dat
      ! default n_bin = 100, and default n_col = n_row = 3
      !
      implicit none
      integer :: n_state, n_bin, n_row, n_col
      double precision, allocatable, dimension(:,:,:) :: total, fin, & 
                                                         tmp_fin
      double precision, allocatable, dimension(:) :: maxium
      character(len=2) :: outname
      double precision :: tmp                 
      integer :: i, j, k, j1, k1, bin, column, row, &
                 row_out, column_out, state

      ! remove gs state
      state = n_state - 1
      row = n_row
      column = n_col
      bin = n_bin

      row_out = row * bin
      column_out = column * bin
      
      allocate (maxium(state)) 
      allocate (total(state,row,column)) 
      allocate (fin(state,row_out,column_out))

      allocate (tmp_fin(state,row_out,column_out))

      do i=1,state 
         write(outname,'(i2)') i 
         open(unit=11, file='state_'//trim(adjustl(outname))//'.dat')
         do j=1,row
            read (11,*) total(i,j,:)
         enddo
         close(11)
      enddo 

      do i=1,state
         maxium(i)=total(i,1,1)
         do j=1,row
            do k=1,column
            tmp=maxium(i)-total(i,j,k)
            if (tmp .ge. 0) then
            else
               maxium(i)=total(i,j,k)
            endif
            enddo
         enddo
      enddo
      
!      do i=1,state
!         print *, maxium(i)
!      enddo

      do i=1,state
         do j=1,row_out
            j1 = int((j-1)/bin) + 1
            !j1 = n_row - j1 + 1
            do k=1,column_out
               k1 = int((k-1)/bin) + 1
               !k1 = column - k1 + 1
               fin(i,j,k) = total(i,j1,k1)
            enddo
         enddo
         close(11)
      enddo

      tmp_fin = fin

!      do i=1,state
!         do j=1,row_out
!            do k=1,column_out
!               fin(i,j,k) = 0.98 - fin(i,j,k)
!            enddo
!         enddo
!      enddo          

      do i=1,state
         do j=1,row
            do k=1,column_out
               if ( j .ne. row) then
                  do j1 = j*bin, j*bin+3 
                     fin(i,j1,k) = 0
                  enddo
               endif
            enddo
         enddo
      enddo          

      do i=1,state
         do k=1,column
            do j=1,row_out
               if ( k .ne. column) then
                  do k1 = k*bin,  k*bin+3
                     fin(i,j,k1) = 0
                  enddo
               endif
            enddo
         enddo
      enddo          

!      do i=1,state
!         tmp_fin(i,:,:) = maxium(i)
!         do j = 1, row_out
!            do k = 2*bin-4 , 2*bin+4 
!              fin(i,j,k) = 0
!            enddo
!         enddo
!         do j = 2*bin-4, 2*bin+4
!            do k = 1, column_out                
!               fin(i,j,k) = 0
!            enddo
!         enddo
!      enddo



      do i=1,state
         write(outname,'(i2)') i
         open(unit=13, file='state_mod_'//trim(adjustl(outname))//'.dat')
         do j=1,row_out
            do k=1,column_out
               write(13,'(1x, i6)',advance="no") j
               write(13,'(1x, i6)',advance="no") k
!               write(13,'(1x, f13.8)') fin(i,j,k)
!               write(13,'(1x, f13.8)', advance="no") fin(i,j,k)
               write(13,'(1x, f13.8)' ) fin(i,j,k)
            enddo
               write(13,*)
         enddo
         close(13)
      enddo
!
      deallocate (total)
      deallocate (fin)
      deallocate (maxium)

    end subroutine sub_contour

!program main
!  call sub_contour(20, 100, 3, 3)
!end


