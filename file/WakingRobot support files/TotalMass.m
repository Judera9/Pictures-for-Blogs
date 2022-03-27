function m = TotalMass(idx)
global uLINK

if idx == 0
    m = 0;
else
    m = uLINK(idx).m + TotalMass(uLINK(idx).sister) + TotalMass(uLINK(idx).child);
end
