clear;clc;
global uLINK
% assign attributes, idx start from 1
uLINK = struct('name', 'BODY', 'm', 20, 'sister', 0, 'child', 2);
uLINK(2) = struct('name', 'RARM', 'm', 5, 'sister', 4, 'child', 3);
uLINK(3) = struct('name', 'RHAND', 'm', 1, 'sister', 0, 'child', 0);
uLINK(4) = struct('name', 'LARM', 'm', 5, 'sister', 6, 'child', 5);
uLINK(5) = struct('name', 'LHAND', 'm', 1, 'sister', 0, 'child', 0);
uLINK(6) = struct('name', 'RLEG', 'm', 10, 'sister', 8, 'child', 7);
uLINK(7) = struct('name', 'RFOOT', 'm', 2, 'sister', 0, 'child', 0);
uLINK(8) = struct('name', 'LLEG', 'm', 10, 'sister', 0, 'child', 9);
uLINK(9) = struct('name', 'LFOOT', 'm', 2, 'sister', 0, 'child', 0);
PrintLinkName(1)
TotalMass(1)

function PrintLinkName(idx)
global uLINK
% this is a preorder traversal
if idx ~= 0
    fprintf('j=%2d : %s\n', idx, uLINK(idx).name);
    PrintLinkName(uLINK(idx).child);
    PrintLinkName(uLINK(idx).sister);
end
end

function m = TotalMass(idx)
global uLINK
if idx == 0
    m = 0;
else
    m = uLINK(idx).m + TotalMass(uLINK(idx).sister) + TotalMass(uLINK(idx).child);
end
end