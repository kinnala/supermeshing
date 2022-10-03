module mainmod

use libsupermesh
implicit none
contains

function foo(p1, t1, p2, t2) result(b)

  use libsupermesh_intersection_finder, only : intersections, deallocate, &
    & intersection_finder
  use libsupermesh_precision, only : real_kind
  use libsupermesh_read_triangle, only : read_ele, read_node
  use libsupermesh_supermesh, only : intersect_elements, &
    & intersect_simplices, triangle_area
  use libsupermesh_tri_intersection, only : tri_type, tri_buf_size, &
       & intersect_tris, intersect_polys, get_lines
  use libsupermesh_unittest_tools, only : report_test, operator(.fne.)
  
  implicit none
  
  real(kind=8), intent(in)    :: p1(:,:)
  integer, intent(in)    :: t1(:,:)
  real(kind=8), intent(in)    :: p2(:,:)
  integer, intent(in) :: t2(:,:)
  real(kind=8) :: b(size(p1,1), 30*size(p1,2))
  integer :: ele_a, ele_b, ele_c, i, n_tris_c
  integer, dimension(:, :), allocatable :: enlist_a, enlist_b
  real(kind = real_kind), dimension(2, 3) :: tri_a_real
  real(kind = real_kind), dimension(2, 3, tri_buf_size) :: tris_c_real
  real(kind = real_kind), dimension(:, :), allocatable :: positions_a, &
    & positions_b  
  type(intersections), dimension(:), allocatable :: map_ab
  type(tri_type) :: tri_a, tri_b
  type(tri_type), dimension(tri_buf_size) :: tris_c
  integer :: k

  b = 0 * b
  ! print *, b
  positions_a = p1
  enlist_a = t1
  positions_b = p2
  enlist_b = t2
  
  allocate(map_ab(size(enlist_a, 2)))
  call intersection_finder(positions_a, enlist_a, positions_b, enlist_b, map_ab)

  k = 1
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      call intersect_elements(tri_a_real, positions_b(:, enlist_b(:, ele_b)), tris_c_real, n_tris_c)
      do ele_c = 1, n_tris_c
         b(:, k:(k+2)) = tris_c_real(:, 1:3, ele_c)
         k = k + 3
      end do
    end do    
  end do

  b(2, 30*size(p1,2)) = k
  
  call deallocate(map_ab)
  deallocate(map_ab, positions_a, enlist_a, positions_b, enlist_b)


 



end function foo

end module mainmod
