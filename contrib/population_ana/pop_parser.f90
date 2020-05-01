  
  subroutine pop_parser (i_job) 
    implicit none
    
    logical alive
    character(len=100) :: filename 
    
    integer :: n_state, n_block, n_atom, n_bin, n_row, n_col
    integer :: i_job

    ! check file status
    filename = "fort.52"    
    inquire(file = filename, exist = alive)
    if (.not. alive) then
       write(*, *) filename, "do not exist."
       stop
    end if

    filename = "block.in"
    inquire(file = filename, exist = alive)
    if (.not. alive) then
       write(*, *) filename, "do not exist."
       stop
    end if

    ! 
    write(*,*) "how many states (INCLUDE ground state)? "
    read(*,*) n_state

    write(*,*) "how many atoms? "
    read(*,*) n_atom

    write(*,*) "how many blocks? "
    read(*,*) n_block    
    n_row = n_block
    n_col = n_block

    if (i_job > 0) then
       write(*,*) "how man bins [i.e. 100]?"
       read(*,*) n_bin
    end if

    if (i_job == 0) then
       write(*,*) "running fragit"
       write(*,*) n_state, n_atom, n_block
       call sub_fragit (n_state, n_atom, n_block, 3)
    end if

    if (i_job == 1) then
       write(*,*) "running counter"
       call sub_contour(n_state, n_bin, n_row, n_col)
    end if
    
    if (i_job == 2) then 
       write(*,*) "running both.."
       write(*,*) "running fragit"
       call sub_fragit (n_state, n_atom, n_block, 3)
       write(*,*) "running counter"
       call sub_contour(n_state, n_bin, n_row, n_col)
    end if

end subroutine


program main
  write(*,*) "fragit(0) or contour(1) or both(2).? > "
  read(*,*) i_job

  call pop_parser(i_job)

  end
