import time


class _Profiler:
    
    def __init__(self):
        self.profiles = {}
        self.current_profile = None
        self.start = None
    
    def __call__(self, *args, **kwargs):
        
        if self.current_profile is not None:
            self.profiles[self.current_profile].append(time.perf_counter() - self.start)
            self.current_profile = None
        
        if args:
            name = args[0]
            
            self.current_profile = name
            self.start = time.perf_counter()
            if name not in self.profiles:
                self.profiles[name] = []
        
    def results(self):
        
        # print(self.profiles)
        
        for profile in self.profiles:
            vals = self.profiles[profile]
            pmin, pmax, pmean, psum = min(vals), max(vals), sum(vals) / len(vals), sum(vals)
            
            print('{:<40}: min {:>8.02f}ms, max {:>8.02f}ms, avg {:>8.02f}ms, total {:>8.02f}ms'.format(
                profile, pmin * 1000, pmax * 1000, pmean * 1000, psum * 1000))
        
        
profile = _Profiler()


if __name__ == '__main__':
    
    profile('first profile')

    time.sleep(0.3)
    
    profile()
    
    profile('first profile')
    
    time.sleep(0.1)
    
    profile('second profile')
    
    time.sleep(0.2)
    
    profile()
    
    profile.results()