# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model
import visualize_solution

class GreenhouseScheduler:

    # The GreenhouseScheduler class takes the following parameters:
    # behaviors_info: a dictionary whose keys are behavior names and whose
    #  values are tuples (t, s, m), where:
    #  t: the least cumulative amount of time in minutes that the behavior
    #     needs to be run
    #  s: the spacing between the behaviors in minutes (min, max)
    #     s.t. <= 1 run in min time and >= 1 in max time
    #     This is used only for some behaviors: (LowerTemp, LowerHumid,
    #     LowerMoist, TakeImage, RaiseTemp, RaiseMoist) and not for any other
    #  m: the maximum amount of time the behavior should run at night
    #     between [20,24) U [0,8)
    # minutes_per_chunk: the number of minutes that the day is broken into
    # sched_file: the name of the file the schedule is to be written to

    def __init__(self, behaviors_info, minutes_per_chunk, sched_file=None,
                 max_constraint=4):
        self.behaviors_info = behaviors_info
        self.minutes_per_chunk = minutes_per_chunk #all are the same length
        self.horizon = 24*60//self.minutes_per_chunk
        self.sched_file = sched_file
        self.createModel(max_constraint)

    def createVariables (self):
        # Create behavior/time dictionary mapping to binary variables.
        self.all_jobs = {}
        for behavior in self.behaviors_info:
            for time in range(self.horizon):
                suffix = '%s_%i' % (behavior, time)
                # Boolean variable for whether behavior is enabled at that time
                self.all_jobs[behavior,time] = self.model.NewBoolVar(suffix)

    def createModel (self, max_constraint=4):
        # Create the model.
        self.model = cp_model.CpModel()
        self.createVariables()
        if (max_constraint >= 1): self.createDurationConstraints(self.model)
        if (max_constraint >= 2): self.createMutualExclusiveConstraints(self.model)
        if (max_constraint >= 3): self.createNightConstraints(self.model)
        if (max_constraint >= 4): self.createSpacingConstraints(self.model)

    # This is the function to call to test the problem being solved.
    # It takes the requirements from the class constructor
    # DO NOT ALTER THIS FUNCTION!
    def solveProblem(self, visualize=False, verbose=False):
        return self.solve(self.model, visualize, verbose)

    # CREATE and add constraints for the minimum duration each behavior
    #     should be run (see self.behaviors_info)
    def createDurationConstraints(self, model):
        for behavior in self.behaviors_info:
            duration = self.behaviors_info[behavior][0] # in minutes
            # BEGIN STUDENT CODE
            # END STUDENT CODE
            pass

    # CREATE and add constraints for behaviors that cannot be run
    #   simultaneously for each time
    # 1. All raising and lowering behaviors for the same value (temperature,
    #    humidity, moisture) must be mutually exclusive
    # 2. Any two behaviors in this list that need to use the same
    #    actuator on (e.g., LowerHumid, LowerMoist) or in which one wants the
    #    actuator on and one wants it off (e.g., LowerHumid and RaiseTemp)
    #    must be mutually exclusive (note: they are not exclusive if they
    #    both need the actuator off)
    #      LowerTemp: fan on, lights off
    #      RaiseTemp: lights on, fan off
    #      LowerHumid: fan on, wpump off
    #      LowerMoist: fan on, wpump off
    #      RaiseMoist: fan off, wpump on
    #      Lights: lights on
    #      TakeImage: lights on
    def createMutualExclusiveConstraints(self,model):
        for time in range(self.horizon):
            # BEGIN STUDENT CODE
            # END STUDENT CODE
            pass

    # CREATE and add constraints for maximum amount of time behaviors should
    # be run at night between [20,24) U [0,8)
    def createNightConstraints(self, model):
        for behavior in self.behaviors_info:
            max_night = self.behaviors_info[behavior][2] # in minutes
            # BEGIN STUDENT CODE
            # END STUDENT CODE
            pass

    # Create and add constraints so that the minimum spacing between behaviors
    #   is the minimum time (given in minutes - convert to chunks), and at least
    #   one behavior is scheduled to run before the maximum time is up
    # If the maximum night-time running is zero, apply these constraints only
    #   during the day (8am to 8pm).
    # Also, the maximum constraint does not hold if there is not enough time
    #   before the end time (either midnight or 8pm)
    def createSpacingConstraints(self,model):
        for behavior in self.behaviors_info:
            chunk = self.minutes_per_chunk
            min_spacing, max_spacing = self.behaviors_info[behavior][1]
            # BEGIN STUDENT CODE
            # END STUDENT CODE

    # Solve model.
    def solve(self,model, visualize, verbose):
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.INFEASIBLE:
            if verbose: print("infeasible")
            return None
        else:
            save = self.sched_file != None
            if verbose: print("feasible")
            assigned_jobs_list = {}
            i =0
            blist = self.behaviors_info.keys()

            if save: f = open(self.sched_file,"w")

            # (optionally) print and write out the schedule
            for behavior in blist:
                if verbose: print("Behavior:",behavior)
                s = "  Times: "
                for t in range(self.horizon):
                    if solver.Value(self.all_jobs[behavior,t]) > 0:
                        assigned_jobs_list[i,i,t/2.] = 1
                        s += str(t/2.)+" "
                        if save: 
                            f.write(behavior+"Behavior"+" ")
                            f.write(("0" if t/2 < 10 else "")+str(int(t//2))+
                                    (":00" if t/2 == t//2 else ":30")+"-")
                        x = t + 1
                        if save:
                            f.write(("0" if x/2 < 10 else "")+str(int(x//2))+
                                    (":00" if x/2 == x//2 else ":30")+"\n")
                if verbose: print(s)
                if save: f.write("\n")
                i += 1

            # Finally print the solution found.
            if status == cp_model.OPTIMAL:
               if verbose: print('Student Optimal Schedule Length: %i' % solver.ObjectiveValue())
            if visualize:
                visualize_solution.plot_binary(blist, self.horizon/2, False, 0.5, assigned_jobs_list)
            return assigned_jobs_list

if __name__ == "__main__":
    # This is an example Schedule generation problem

    #schedule 30 minute chunks
    minutes = 30
    behaviors_info = {}

    # Light should be on for at least 8 hours during the day (not on at night)
    #   Instances can be scheduled back-to-back (0 min time) but
    #   at least every 4 hours during the day
    behaviors_info = {}
    behaviors_info["Light"] =      (8*60,(0,    4*60), 0)
    behaviors_info["LowerHumid"] = (8*60,(30,   2*60), 12*60)
    behaviors_info["LowerTemp"] =  (4*60,(2*60, 4*60), 12*60)
    behaviors_info["RaiseTemp"] =  (2*60,(2*60, 4*60), 12*60)
    behaviors_info["LowerMoist"] = (2*60,(2*60, 4*60), 12*60)
    behaviors_info["RaiseMoist"] = (2*60,(2*60, 4*60), 12*60)
    # camera should not be on at all at night
    behaviors_info["TakeImage"] =  (1*60,(3*60, 6*60),  0)

    problem = GreenhouseScheduler(behaviors_info, minutes, "main_schedule.txt")
    problem.solveProblem(visualize=True)

