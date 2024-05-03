from typing import List
from dataclasses import dataclass

@dataclass
class Index:
    a: int
    b: int


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    m, n = len(nums1), len(nums2)
    mid = int((m + n - 1) / 2)

    def index(idx: int) -> Index:
        i = Index(a=0, b=0)
        while True:
            i.b = idx - i.a
            print('@1', nums1, nums2, i.a, i.b)
            if i.a == m:
                break
            if ((i.b <= 0 or nums2[i.b - 1] <= nums1[i.a]) and
                (i.b >= n - 1 or nums1[i.a] <= nums2[i.b + 1]) and
                (i.a <= 0 or nums1[i.a - 1] <= nums2[i.b]) and
                (i.a >= m - 1 or nums2[i.b] <= nums1[i.a + 1])):
                break
            i.a += 1
        return i

    def value_at(idx: Index) -> float:
        i = index(idx)
        if m <= i.a:
            return nums2[i.b]
        if n <= i.b:
            return nums1[i.a]
        return min(nums1[i.a], nums2[i.b])

    if (m + n) % 2 == 1:
        return value_at(mid)
    else:
        return (value_at(mid) + value_at(mid + 1)) / 2



def test_len1():
    assert findMedianSortedArrays([7], []) == 7

def test_len1_reverse():
    assert findMedianSortedArrays([], [7]) == 7

def test_overlap():
    assert findMedianSortedArrays([1, 3], [2]) == 2

def test_concat():
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5

def test_concat2():
    assert findMedianSortedArrays([1, 2], [3, 4, 5, 6, 7, 8]) == 4.5

def test_concat2_odd():
    assert findMedianSortedArrays([1, 2], [3, 4, 5, 6, 7]) == 4

