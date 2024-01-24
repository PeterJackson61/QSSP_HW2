mystartdefaults

tic

dispersion_relation = true, compute_dos = false;

CohenBergstresser1966

recipunit = 1.e+10
ekinscale = ((hbar*recipunit)^2/(2*elm))/qel

%%Set ouput filename

file_name = sprintf('%s_Bands.dat', materials{m});
f1 = fopen(file_name, 'w')

%UNIT VECTOR IN RECIPROCAL SPACE EQUATION 1.17

g = zeros(4,3);
g(1:3,1) = cross(a(:,2),a(:,3))/cell_volume;
g(1:3,2) = cross(a(:,3),a(:,1))/cell_volume;
g(1:3,3) = cross(a(:,1),a(:,2))/cell_volume;

for i=1:3
  g(4,i) = g(1:3,i)'*g(1:3,i);
end
g

% BUILD RECIPROCAL LATTICE

min_norm = sqrt(min(g(4,:)))
nstep = ceil(sqrt(cutoff)/min_norm)
fprintf(['cutoff requires %d positive steps along each repc lattice unit vector \n'], nstep);

nodes = (2*nstep+1)^3;
fprintf(['Generate (2+%1d +1)^3 = %4d reciprocal lattice vector\n'], nstep, nodes)

G = zeros(5,nodes);
n=0;

for nx = -nstep:nstep
    for ny = -nstep:nstep
        for nz = -nstep:nstep
            n=n+1;
            G(1:3,n) = nx*g(1:3, 1) + ny*g(1:3, 2) + nz*g(1:3, 3);
            G(5,n) = G(1:3,n)'*G(1:3,n);
            G(4,n) = sqrt(G(5,n));
        end
    end
end

GT = sortrows(G',4);
G = GT'

% Keep G vectors inside cutoff radius
printtable(G')

%G(5,:)'
kept = 1 ;
for n=2:nodes
  if G(5,n)<=cutoff
    kept = kept + 1;
  end
end

fprintf('%4d G vectors featuring G^2 < cutoff',kept);
if kept < nband
  nband = kept
end

if m~= 15

%Calculate the fourier coeff

  spacing = ls(m)
  ekinunit = ekinscale*(2*pi/spacing)^2

  for n=1:kept
    sym = 0 ;
    asym = 0;

    if G(5,n) == 0
      sym = ff(m,1)*Rydberg;
      asym = 0;
    end
    if G(5,n) == 3
      sym = ff(m,2)*Rydberg;
      asym = ff(m,5)*Rydberg;
    end
    if G(5,n)==4
      sym = 0;
      asym = ff(m,6)*Rydberg;
    end
    if G(5,n) == 8
      sym = ff(m,3)*Rydberg;
      asym = 0;
    end
    if G(5,n) == 11
      sym = ff(m,4)*Rydberg;
      asym = ff(m,7)*Rydberg;
    end

    argu = 2*pi* (G(1:3,n)'*tau(1:3,1));
    cvg(n) = cos(argu)*sym-1i*sin(argu)*asym;

  end
end

Fourier_coeff_file = sprintf('%s_Fourier_Coeff.dat',materials{m});
f0 = fopen(Fourier_coeff_file,'w');

for fid = [1 f0]
   fprintf(fid, '\n Table of G vectors [2*pi/spacing]');
   fprintf(fid,'And fourier coefficients of psudopotential [eV]\n');
   fprintf(fid,'      n            G(1)          G(2)              G(3)');
   fprintf(fid,'           |G|             |G|^2           Re(V_G)           Im(V_G)\n');
   for n = 1:kept
     fprintf(fid, ' %4d %15.6G %15.6G %15.6G %15.6G %15.6G %15.6G %15.6G\n', n, G(1:5,n),real(cvg(n)),imag(cvg(n)));
   endfor
end
fclose(f0);


# HAMILTONIAN OFF-DIAGONAL ELEMENTS
% = Fourier components of potential energy

H = zeros(kept,kept); %Initialization of Hamiltonian matrix
G_diff=zeros(5,1);    %Initialization as column vector

for j= 1:kept
  for i= 1:kept
    G_diff(1:3) = G(1:3,i)-G(1:3,j);
    G_diff(5) = G_diff(1:3)'*G_diff(1:3);
    if(G_diff(5)<=Gs_max)
      for k=1:kept
        if(norm(G_diff(1:3)-G(1:3,k))< tol)
          H(i,j) = cvg(k);
        end
      end
    end
  end
end

# HERMITIAN TEST

if(~ishermitian(H,tol))
   error('Hamiltonian matrix is not hermitian: fatal error');
end

% Output file

file_name = sprintf('%s_Bands.dat',materials{m});
f1 = fopen(file_name,'w');

% Wavevectors along path in BZ

[q,~,~]=BZpath(BZstep,qs,qe,qs_str,qe_str);
[~,nq]=size(q);

% Initialize bandstructure matrix
%bandstructure = zeros(nband, nq);

fprintf('Diagonalization loop over %4d wavevectors\n', nq);

for iq = 1:nq
    % Kinetic energy
    for i = 1:kept
        for j = 1:3
            p(j) = q(j,iq) - G(j,i);
        endfor
        H(i,i) = ekinunit*(p*p') + cvg(1);
    endfor

    % Diagonalization
    [v, ev] = eig(H);
    E = real(diag(ev));
    [E, perm] = sort(E);
    v = v(:, perm);

    % output to the file

    bzs = (-1)^q(6,iq); % to allow drawing boundaries of segments of the path in BZ

    fprintf(f1, '%15.6G %15.6G',q(5,iq),bzs); % abscissa and segment identifier

    for i =1:nband
      fprintf(f1,'%15.6G',E(i)); % Lowest nband eigenvalues
    endfor
    fprintf(f1,'\n');
    % Eigenvalue at gamma point
    if(q(4,iq)==0)
       for i = 1:nband
         gamma(i,iq) = E(i);
       endfor
    end
end

fclose(f1);














































