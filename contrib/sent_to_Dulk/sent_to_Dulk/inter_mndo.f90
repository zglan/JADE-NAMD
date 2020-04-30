! This script is used to translate xyz geometries to mndo readable ones.
! H is 1, C is 6, N is 7, O is 8.   
      program main
      implicit none
      character*10 aa
      double precision, allocatable :: x_1(:), y_1(:), z_1(:)
      double precision, allocatable :: x_2(:), y_2(:), z_2(:)
      double precision, allocatable :: x_e(:), y_e(:), z_e(:)
      double precision, allocatable :: dx(:), dy(:), dz(:)
 



      integer ::              n_atom, n_step, atom_num    
      integer, allocatable :: num_1(:), num_2(:)
      integer, allocatable ::  label_1_1(:), &
                                                 label_1_2(:), &
                                                 label_1_3(:), &
                                                 label_1_4(:), &
                                                 label_1_5(:), &
                                                 label_1_6(:)
      integer,           allocatable  ::   label_2_1(:), &
                                                 label_2_2(:), &
                                                 label_2_3(:), &
                                                 label_2_4(:), &
                                                 label_2_5(:), &
                                                 label_2_6(:)
      character (len=50) :: file1
      character (len=50) :: file2
      character (len=50) :: file3
      character (len=50) :: file4
      character, allocatable ::   atom_1(:), atom_2(:)
      character ::  tmp_atom
      integer :: i, j       


      
       
       read (*,*) n_atom
       read (*,*) file1
       read (*,*) file2
       read (*,*) n_step


       allocate (num_1(n_atom))
       allocate (num_2(n_atom))

       allocate (x_1(n_atom))
       allocate (y_1(n_atom))
       allocate (z_1(n_atom))
       
       allocate (x_2(n_atom))
       allocate (y_2(n_atom))
       allocate (z_2(n_atom))
   
       allocate (x_e(n_atom))
       allocate (y_e(n_atom))
       allocate (z_e(n_atom))

       allocate (dx(n_atom))
       allocate (dy(n_atom))
       allocate (dz(n_atom))


       allocate (atom_1(n_atom))
       allocate (atom_2(n_atom))




       allocate (label_1_1(n_atom))
       allocate (label_1_2(n_atom))
       allocate (label_1_3(n_atom))
       allocate (label_1_4(n_atom))
       allocate (label_1_5(n_atom))
       allocate (label_1_6(n_atom))

       allocate (label_2_1(n_atom))
       allocate (label_2_2(n_atom))
       allocate (label_2_3(n_atom))
       allocate (label_2_4(n_atom))
       allocate (label_2_5(n_atom))
       allocate (label_2_6(n_atom))






        open (unit=15,file=trim(file1),status='unknown', &
              access='sequential', form='formatted')
        open (unit=16,file=trim(file2),status='unknown', &
          access='sequential', form='formatted')


 
         
      


       do j=1, n_step

          read (15,*) 
          read (15,*) 
 
          do i=1,n_atom
             read (15,*) atom_1(i), x_1(i),  &
                                    y_1(i),  &
                                    z_1(i) 
          enddo

          do i=1, n_atom

             if (  atom_1(i)  .eq. "H"  ) then
                 num_1(i)=1
             endif

             if (  atom_1(i)  .eq. "C"  ) then
                 num_1(i)=6
             endif

             if (  atom_1(i)  .eq. "N"  ) then
                num_1(i)=7
             endif

             if (  atom_1(i)  .eq. "O"  ) then
                num_1(i)=8
             endif

          enddo


          label_2_1(:)=1
          label_2_2(:)=1
          label_2_3(:)=1



             write (16, * )"--------------------------"
             write (16, * ) "Point", j
             write (16, * )"--------------------------"

          do i=1, n_atom
             write (16,9995)  num_1(i), x_1(i),  label_2_1(i), &
                                        y_1(i),  label_2_2(i), &
                                        z_1(i),  label_2_3(i)
          enddo


       enddo
        
9995   format(i2, 2x, 3(f10.5, 2x, i2, 2x)  )

       
       close (15)
       close (16)
        
       end
       


