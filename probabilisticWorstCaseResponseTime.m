function [ respTime ] = probabilisticWorstCaseResponseTime( taskSet, nbOfPeriods )

%computes the response time distribution of the least prioritary task in a given taskset in a study interval, the study interval is given as a multimple of the larget arrival time values of the least prioritary task. if nbOfPeriods is equal to 1, then the analysis is performed up to the deadline of te task. 



format longE

target = length(taskSet);
respTime=taskSet{target}{1};


for i=1:target-1
    respTime = dcf(respTime,taskSet{i}{1});
end

respTime = resampling(respTime,100);

interval = {};

for i=1:target-1
    interval{i} = taskSet{i}{2};
    %interval{i} = periodResampling(interval(i), 10)
end



for i=1:nbOfPeriods*max(taskSet{target}{2}(1,:))   
    
    for j=1:target-1
        
        if max(respTime(1,:)) > min(interval{j}(1,:)) && floor(min(interval{j}(1,:))) == i            
            respTime = doPreemption(respTime, interval{j}, taskSet{j}{1});
            
			%uncomment the next line if you want to resample the response time after each preemption . the second parameter is the number of samples to be kept
            respTime = resampling(respTime,100);
            
            interval{j}=dcf(interval{j},taskSet{j}{2});
			
			%%uncomment the next line if you want to resample the arrival time distribution of the next job . the second parameter is the number of samples to be kept
            %interval{j} = periodResampling(interval{j}, 5);
            
            
            
        end
        
    end
    
    
end


respTime  = sortRandVar(respTime);


%uncomment one of the next lines if you want to do a plot of the response time distribution
%bar(respTime(1,:), respTime(2,:))





end

