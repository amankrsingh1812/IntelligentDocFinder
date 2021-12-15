from queue import Queue
from threading import Thread


class DistributedPipeline:
    _sentinel = object()
    
    def __init__(self, file_iterator, stage_functions, accumulator, num_workers = 1):
        """
        if there are n stage_functions, then
            number of input queues required = n + 1
                -> 1st queue initialised by file_iterator
                -> output of last stage will be in pipeline_output 
        """
        self.stage_functions = stage_functions
        self.accumulator = accumulator
        self.num_workers = num_workers
        self.file_iterator = file_iterator
        
        self.message_queues = [Queue() for i in range(1+len(stage_functions))]
        self.pipeline_output = None
        
        self.stage_zero_threads = []
        self.worker_threads = []
        
        for _ in range(self.num_workers):
            self.stage_zero_threads.append(Thread(
                target = DistributedPipeline.stage_zero_function, 
                args = (file_iterator, self.message_queues[0])
            ))
        
        for (idx, function) in enumerate(self.stage_functions):
            self.worker_threads.append([])
            for _ in range(self.num_workers):
                self.worker_threads[idx].append(Thread(
                    target = DistributedPipeline.worker_thread_function, 
                    args = (self.message_queues[idx], self.message_queues[idx+1], function)
                ))

        
    def run(self):
        self.__reset()
        
        for idx in range(self.num_workers):
            self.stage_zero_threads[idx].start()
            
        for idx_i in range(len(self.stage_functions)):
            for idx_j in range(self.num_workers):
                self.worker_threads[idx_i][idx_j].start()
                
        self.pipeline_output = DistributedPipeline.accumulator_thread_function(
                                                self.message_queues[len(self.stage_functions)], 
                                                self.accumulator,
                                                self.file_iterator.get_num_paras());
        
        self.__finish()
        print('[Testing]: Run completed successfully')
        return self.pipeline_output

    
    def __reset(self):
        for queue in self.message_queues:
            queue.queue.clear()
            
        
    def __finish(self):
        for queue in self.message_queues:
            queue.put(DistributedPipeline._sentinel)
        
        
    @staticmethod
    def stage_zero_function(file_iterator, out_queue):
        while True:
            try:
                data = next(file_iterator)
            except StopIteration:
                # out_queue.put(DistributedPipeline._sentinel)
                break
            out_queue.put(data)

            
    @staticmethod
    def worker_thread_function(in_queue, out_queue, func):
        while True:
            data = in_queue.get()
            if data is DistributedPipeline._sentinel:
                # out_queue.put(data)
                in_queue.put(data)
                break
            
            processed_data = func(data)            
            out_queue.put(processed_data)

            
    @staticmethod    
    def accumulator_thread_function(in_queue, accumulator, num_paragraphs):
        counter = 0
        out = []
        while True:
            data = in_queue.get()
            # if data is DistributedPipeline._sentinel:
            counter += 1
            if counter == num_paragraphs:
                break
                
            processed_data = accumulator(data)
            out += processed_data
        return out