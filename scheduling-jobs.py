

from heap import Heap

class Main:
    def __init__(self):
        super().__init__()
        self.number_of_jobs = None
        self.jobs_weight_length = []
        
    def main(self):
        self.read_input()
        self.schedule_via_difference()
        self.schedule_via_ratio()
        
    # NOTE: not always optimal
    def schedule_via_difference(self):
        heap = Heap()
        for index, job in enumerate(self.jobs_weight_length):
            score = -(job[0] - job[1] + (job[0] / 1000))
            heap.push(index, score)
        
        weighted_competion_times = 0
        previous_jobs_length = 0
        next_job = heap.pop()
        while (next_job):
            next_job_index = next_job[0]
            (job_weight, job_length) = self.jobs_weight_length[next_job_index]
            weighted_competion_times += (previous_jobs_length + job_length) * job_weight
            previous_jobs_length += job_length
            next_job = heap.pop()
        
        print('Via difference')
        print(weighted_competion_times)
        
    def schedule_via_ratio(self):
        heap = Heap()
        for index, job in enumerate(self.jobs_weight_length):
            score = -(job[0] / job[1])
            heap.push(index, score)
        
        weighted_competion_times = 0
        previous_jobs_length = 0
        next_job = heap.pop()
        while (next_job):
            next_job_index = next_job[0]
            (job_weight, job_length) = self.jobs_weight_length[next_job_index]
            weighted_competion_times += (previous_jobs_length + job_length) * job_weight
            previous_jobs_length += job_length
            next_job = heap.pop()
            
        print('Via ration')
        print(weighted_competion_times)
            
    
    def read_input(self):
        text_file = open("scheduling-jobs-input.txt", "r")
        lines = text_file.readlines()
#         lines = """6

# 8 50

# 74 59

# 31 73

# 45 79

# 24 10

# 41 66""".split("\n\n")
        self.number_of_jobs = int(lines[0])
        self.jobs_weight_length = [(int(line.split(" ")[0]), int(line.split(" ")[1])) for line in lines[1:]]
        #self.jobs_weight_length = [[2, 1], [3, 2], [4, 3], [2, 3]]
    
    
Main().main()
        