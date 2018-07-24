class Solution(object):
    def minMoves2(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        [1,2,3]
        [2,2,3]
        [-1,-1,-1]
        """
        length = len(nums)
        min_number = 9999999
        target = 0
        sum_=sum(nums)
        for i in nums:
        	t = abs(sum_ - i * length) 
        	if t < min_number:
        		min_number = t
        		target = i
        return sum([abs(x-target) for x in nums])
        
class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        [1,2,2,3]
        [2,2]
        """
        return [x for x in nums1 if x in nums2]


def fb(n):
	count = 0
	if n ==1 or n== 0:
		count = 1
	else:
		count =  fb(n-2) + fb(n-1)
	return count


