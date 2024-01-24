function printtable(a,varargin)
    
%% ROW-WISE PRINTING OF A NUMERICAL ARRAY IN SCIENTIFIC NOTATION
%  thereby defining the precision as the number of significant digits
    
%% INPUTS

%  a(1:m,1:n) = mXn array to be printed row-wise
    
%% Recognized options in varargin 
% (uppercases for readability are optional): 

% if varargin{k} = 'Precision', 
%                   then varargin{k+1} = array p = [p(1) p(2) p(3) ...]
%                = number of significant digits in the mantissae, i.e.:
%                   p(i) is the precision of a(:,i)
%                   If lp=length(p) < n=columns(a), 
%                   then p(lp) is the precision of a(:,lp:n)
%    
% if varargin{k} = 'Integer', 
%                   then varargin{k+1} = array = [i j k ...]
%                                      = indices of columns 
%                                         to be displayed as integers
% if varargin{k} = 'Normalized', 
%                   then varargin{k+1} = Boolean to use normalized 
%                                        scientific notation or not
% if varargin{k} = 'StartOfLine', 
%                   then varargin{k+1} = character string
%                                      = separator before first field
% if varargin{k} = 'Separator', 
%                   then varargin{k+1} = character string
%                                      = separator between fields
% if varargin{k} = 'EndOfLine', 
%                   then varargin{k+1} = character string
%                                      = separator after last field
% if varargin{k} = 'HTML', 
%                   then varargin{k+1} = Boolean to use HTML table
%                                        format or not  
% if varargin{k} = 'LaTeX', 
%                   then varargin{k+1} = Boolean to use LaTeX tabular
%                                        format or not         
% if varargin{k} = 'LineNumber', 
%                   then varargin{k+1} = Boolean to number lines 
%                                        or not 
% if varargin{k} = 'FirstLine', 
%                   then varargin{k+1} = start of line number
%                                        counter  
% if varargin{k} = 'Title', 
%                   then varargin{k+1} = character string 
%                                      = Title of table
% if varargin{k} = 'ArrayName', 
%                   then varargin{k+1} = character string
%                                      = array name to print in
%                                        column headers
% if varargin{k} = 'OutputFile', 
%                   then varargin{k+1} = identifier of output file
%                                        (default = screen)
    
%% DEFAUT VALUES OF OPTIONAL ARGUMENTS

p(1)=6;     % Number of significant digits in the mantissa
sep=' ';    % Separator between fields
sol=sep;    % Start of line separator
eol=sep;    % End of line separator
firstline=1;% Numbering of the first line  
intx=[];    % No column displayed as integer
Title=[];   % Empty title
fileID=1;   % Reserved file handle for screen output
normalized=false; linenumber=false; 
printtitle=false; columntitles=false;
html=false; latex=false; 

%% PARSE OPTIONAL ARGUMENT LIST

% NB: To prepare the later understanding of the Matlab/Octave parsing
%     tools (addRequired, addOptional addParameter), parsing  of
%     optional arguments is developped explicitly in this example.

name_value_pair=false;
for k = 1:length(varargin)
    if (name_value_pair)
        name_value_pair=false;
    else
        switch lower(varargin{k}) % varargin is a cell array
          case {'precision'}
            p = varargin{k+1}; name_value_pair=true;
          case {'integer'}
            intx = varargin{k+1}; name_value_pair=true;
          case {'normalized'}
            normalized=varargin{k+1}; name_value_pair=true;
          case {'startofline'}
            sol = varargin{k+1}; name_value_pair=true;
          case {'separator'}
            sep = varargin{k+1}; name_value_pair=true;
          case {'endofline'}
            eol = varargin{k+1}; name_value_pair=true;
          case {'html'}
            html = varargin{k+1}; name_value_pair=true;
            sol='<tr align="right"><td>'; sep='</td><td>'; eol='</td></tr>';
          case {'latex'}
            latex = varargin{k+1}; name_value_pair=true;
            sol=' '; sep=' & '; eol=' \\';
          case {'linenumber'}
            linenumber=varargin{k+1}; name_value_pair=true;
          case {'firstline'}
            firstline = varargin{k+1}; name_value_pair=true;
          case {'title'}
            printtitle=true;
            Title=varargin{k+1}; name_value_pair=true;
          case {'arrayname'}
            columntitles=true;
            C=varargin{k+1}; name_value_pair=true;
          case {'outputfile'}
            name_value_pair=true;
            fileID=fopen(varargin{k+1},'w');
          otherwise
            error('option %s not recognized',varargin{k});
        end
    end
end

%% CHECK INPUT CONSISTENCY

lp=length(p);

for i=1:lp
    if (p(i)~=floor(p(i)) || p(i)<1 || p(i)>15)
        error('Precision of column %d must be an integer between 1 and 15.',i)
    end
end

if (length(sep) > 4)
    error('Separator length must be between 1 and 4.')
end

if (html && latex)
   error('HTML and LaTeX outputs can not be requested simultaneously.')
end

%% CORE JOB

m=rows(a); n=columns(a); l=sprintf('%d',ceil(log10(m)));

if(lp>n)
    p(n+1:end)=[]; % Discard input in excess
end

if (lp<n)
    for i=lp+1:n
        p(i)=p(lp); % Complete if abbreviated input
    end
end

if (normalized)
    f='E'; % Normalized scientific notation forces decimal point after
           % first significant digit
else
    f='G'; % Scientific notation with floating position of decimal point
end

%% Width of data fields

% For each column i,
% width(i) = Number of characters to print a floating-point number =
%  + Mantissa with p(i) significant digits: p(i)
%  + Sign of mantissa: 1  
%  + Decimal point:    1  
%  + Exponent flag:    1  
%  + Sign of exponent: 1  
%  + Exponent value:   3  
%  + character(s) separating fields > 0   

for i=1:n
    width(i)=p(i)+7+length(sep);
    s{i}=sprintf('%d',p(i)); 
    w{i}=sprintf('%d',width(i)); 
end

%% Begin environment

if (printtitle && ~html && ~latex)
    fprintf(fileID,'\n%s\n',Title)
end

if (html)
    fprintf('HTML formatting of table\n\n')
    fprintf(fileID,'<table border="2" cellspacing="2" cellpadding="2">\n')
    fprintf(fileID,'<caption>%s</caption>\n',Title)
end

if (latex)
    fprintf('LaTeX formatting of table\n\n')
    fprintf(fileID,'\\begin{table}\n\\begin{tabular}{|')
    for j=1:n
        fprintf(fileID,'r|') % right alignment
    end
    fprintf(fileID,'}\n\\hline\n')
end

%% Columns' headers

if(columntitles)  
    for j=1:n
        if(length(C)>width(j)-5-ceil(log10(n)))
            C(2:end)=[];
            warning(['for display, too long array name ' ...
                     'has been shortened to %s'],C)
        end
    end
    
    for j=2:n
        B=' ';
        for i=1:width(j)-5-length(C)
            B=[B ' '];
        end
        k=length(B)-ceil(log10(j));
        D{j}=B(1:k);
    end
    D{1}=D{2};
    
    fprintf(fileID,'%s',sol)
    if(linenumber)
        fprintf(fileID,['%' l 's' sep],'n')
    end   
    for j=1:n-1
        fprintf(fileID,'%s%s(%d,n)%s',D{j},C,j,sep)
    end
    fprintf(fileID,'%s%s(%d,n)%s\n',D{n},C,n,eol)
    if (latex)
        fprintf(fileID,'\\hline\\hline\n')
    end
end

%% Rows

for i=1:m
    fprintf(fileID,'%s',sol)
    if(linenumber)
        fprintf(fileID,['%' l 'd' sep],i+firstline-1)
    end
    for j=1:n-1
        if (ismember(j,intx))
            fprintf(fileID,['%' w{j} '.0f' sep],a(i,j))
        else
            fprintf(fileID,['%#' w{j} '.' s{j} f sep],a(i,j))
        end
    end
    if (ismember(n,intx))
        fprintf(fileID,['%' w{n} '.0f'],a(i,n))
    else
        fprintf(fileID,['%#' w{n} '.' s{n} f],a(i,n))
    end
    fprintf(fileID,'%s \n',eol)
end

%% End of environment

if (html)
    fprintf(fileID,'</table>\n\n')
end

if (latex)
    fprintf(fileID,'\\hline\n\\end{tabular}\n\\begin{caption}\n')
    fprintf(fileID,'%s\n\\end{caption}\n\\end{table}\n\n',Title)
end

if (fileID ~=1)  
    fclose(fileID); 
end

end % End of function printtable
