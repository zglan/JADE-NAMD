      program main
      implicit none
      integer, allocatable, dimension(:) :: state 
                       
      character (len=50) :: file1
      character (len=50) :: file2
      character (len=50) :: file3
      character (len=50) :: file4
      integer :: i, j, time_state, time_angle, i_ci, i_atom,k
      integer :: nstep_state, nstep_geo, n_atom, nn_atom, n_step,&
                 n_qm_atom, fsav
      double precision :: x, y, z, energy
      character (len=10) :: aa, bb, atom_label




!     How many steps
      nstep_state=10000

!     How often to save geometries.
      fsav=100

      nstep_geo=nstep_state/fsav

!     How many atoms
      n_atom=12



      allocate (state(nstep_state))


      open(unit=11, file="state.dat")
      open(unit=13, file="traj.out")
      open(unit=14, file="ci_qm.xyz")



      do i=1,nstep_state 
      read (11,*) time_state, state(i)

        if (state(i)  .eq.  1 ) then
         print *, i
         
         i_ci=int(i/fsav)
         
         print *, i,i_ci


         do k= 1, n_atom+3
         read (13,*)
         enddo


         do k= 1, (i_ci-1) * (n_atom+2)
         read (13,*) 
         enddo
 

          read  (13,*) nn_atom
          read  (13,*)

          write (14,*) nn_atom
          write (14,*) i 



         do k=1, n_atom

         read  (13,*) atom_label, x, y, z
         write (14,9997) atom_label, x, y, z

          enddo
 


        
        


         goto 110
         
      endif




      enddo




9995   format ( a, 3x, a, 3x, i4 )
9996   format ( a, 3x i7, 3x, a, 3x, f14.7 )
9997   format (a, 3(4x, f14.7))

110   print *, i, i_ci

       




       end
