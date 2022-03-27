function PrintLinkName(idx)
global uLINK

% this is a preorder traversal
if idx ~= 0
    fprintf('j=%2d : %s\n', idx, uLINK(idx).name);
    PrintLinkName(uLINK(idx).child);
    PrintLinkName(uLINK(idx).sister);
end