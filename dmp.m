

function [out]=dmp(B,A)

%backlog and deadline miss probability distribution function
%compares two random varibles, A being the response time of a task, and B being the deadline (period) of the same task


if isempty(A)
   A=[0; 1]; 
end

if isempty(B)
   B=[0; 1]; 
end

s=size(A,2);
res=[];
for i =1:s  
    tmp=B-[A(1,i)*ones(1,size(B,2)); 0*ones(1,size(B,2))];
    tmp = tmp .* [1 * ones(1,size(B,2)); A(2,i)*ones(1,size(B,2))];
    res=[res tmp];
end

[t,idx] =sort(res(1,:),2);res=res(:,idx);
init=res(1,1);
out = [];
while (find(res(1,:)==init))
    out=[out [init ;sum(res(2,find(res(1,:)==init)),2)]];
    res(:,find(res(1,:)==init))=[];
    if size(res)
        init = res(1,1);
    end
end


%values less or equal to zero are gathered in zero, they represent idle time. only the pozitive values represent backlog and give the deadline miss probability

rezFinal = zeros(2, 1);

  for i=1:length(out(1,:))
    if out(1,i) <= 0
      rezFinal(2,1) = rezFinal(2,1) + out(2,i);
    else
      rezTemp = [out(1,i); out(2,i)];  
      rezFinal= cat(2,rezFinal,rezTemp);
    end 
  end
  
  out = rezFinal;
  
end