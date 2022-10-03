module mainmod

use libsupermesh
implicit none
contains

function foo(a) result(b)

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
  
  real(kind=8), intent(in)    :: a(:,:)
  complex(kind=8)             :: b(size(a,1),size(a,2))
  integer :: ele_a, ele_b, ele_c, i, n_tris_c
  integer, dimension(:, :), allocatable :: enlist_a, enlist_b
  real(kind = real_kind) :: area_c
  real(kind = real_kind), dimension(2, 3) :: tri_a_real
  real(kind = real_kind), dimension(2, 3, tri_buf_size) :: tris_c_real
  real(kind = real_kind), dimension(2, tri_buf_size + 2, 2) :: work
  real(kind = real_kind), dimension(:, :), allocatable :: positions_a, &
    & positions_b  
  type(intersections), dimension(:), allocatable :: map_ab
  type(tri_type) :: tri_a, tri_b
  type(tri_type), dimension(tri_buf_size) :: tris_c

  integer, parameter :: dim = 2
  
  call read_node("data/triangle_0_01.node", dim, positions_a)
  call read_ele("data/triangle_0_01.ele", dim, enlist_a)
  call read_node("data/square_0_01.node", dim, positions_b)
  call read_ele("data/square_0_01.ele", dim, enlist_b)
  
  allocate(map_ab(size(enlist_a, 2)))
  call intersection_finder(positions_a, enlist_a, positions_b, enlist_b, map_ab)

  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a%v = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      tri_b%v = positions_b(:, enlist_b(:, ele_b))
      call intersect_tris(tri_a, tri_b, tris_c, n_tris_c)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c(ele_c)%v)
      end do
    end do    
  end do
  call report_test("[intersect_tris]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")

  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      call intersect_tris(tri_a_real, positions_b(:, enlist_b(:, ele_b)), tris_c_real, n_tris_c)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c_real(:, :, ele_c))
      end do
    end do    
  end do
  call report_test("[intersect_tris]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")

  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a%v = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      tri_b%v = positions_b(:, enlist_b(:, ele_b))
      call intersect_polys(tri_a, get_lines(tri_b), tris_c, n_tris_c, work = work)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c(ele_c)%v)
      end do
    end do    
  end do
  call report_test("[intersect_polys]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")

  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      call intersect_polys(tri_a_real, get_lines(positions_b(:, enlist_b(:, ele_b))), tris_c, n_tris_c, work = work)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c(ele_c)%v)
      end do
    end do    
  end do
  call report_test("[intersect_polys]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")

  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      call intersect_polys(tri_a_real, positions_b(:, enlist_b(:, ele_b)), tris_c, n_tris_c, work = work)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c(ele_c)%v)
      end do
    end do    
  end do
  call report_test("[intersect_polys]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")
  
  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      call intersect_simplices(tri_a_real, positions_b(:, enlist_b(:, ele_b)), tris_c_real, n_tris_c)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c_real(:, :, ele_c))
      end do
    end do    
  end do
  call report_test("[intersect_simplices]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")
  
  area_c = 0.0_real_kind
  do ele_a = 1, size(enlist_a, 2)
    tri_a_real = positions_a(:, enlist_a(:, ele_a))
    do i = 1, map_ab(ele_a)%n
      ele_b = map_ab(ele_a)%v(i)
      call intersect_elements(tri_a_real, positions_b(:, enlist_b(:, ele_b)), tris_c_real, n_tris_c)
      do ele_c = 1, n_tris_c
        area_c = area_c + triangle_area(tris_c_real(:, :, ele_c))
      end do
    end do    
  end do
  call report_test("[intersect_elements]", area_c .fne. 0.5_real_kind, .false., "Incorrect intersection area")
  
  call deallocate(map_ab)
  deallocate(map_ab, positions_a, enlist_a, positions_b, enlist_b)


 

    b = exp((0,1)*a)

end function foo

end module mainmod
