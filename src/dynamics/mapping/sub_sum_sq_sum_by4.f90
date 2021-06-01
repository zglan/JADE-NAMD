subroutine sub_sum_sq_sum_by4(x1, x2, x3, x4, rresult)
implicit none
real(kind=8) x1, x2, x3, x4, rresult

rresult = ((x1 + x2)**2 + (x3 - x4)**2)/4.d0

return
end
