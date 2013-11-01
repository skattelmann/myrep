#INPUT: 'polytope.txt' beinhaltet das "Pyramiden-Fundament" (als Matrix der Ecken) und 'inequalities.txt' beinhaltet die Ungleichungen für mögliche "Spitzen" der Pyramide. 
#       Die Ungleichungen haben grundsätzlich die Form const + x_1 e_1 + ... + x_n e_n >= 0, wobei const und die x_i in der Datei in jeweils einer Zeile stehen. 
#       Die letzte Zeile von 'polytope.txt' ist immer eine Zeile mit 0-Einträgen.
#       ARG1 entspricht der Zahl von geforderten inneren Gitterpunkten, ARG2 ist der geforderte Gitterdurchmesser und ARG 3 entspricht der Wahl der Ungleichheit für den GDM, daher 0 für "<" und 1 für ">"
# 	Ein möglicher Befehl für den Start des Programms: "polymake --script /home/.../testscript.pl polytope.txt inequalities.txt 13 2 1".
# 	Für polytope.txt und inequalities.txt sind Beispieldateien vorhanden.

#OUTPUT:Alle Pyramiden mit den geforderten Eigenschaften. Diese werden auf der Konsole ausgegeben.

ARG1 entspricht der Zahl von geforderten Gitterpunkten, ARG2 ist der geforderte Gitterdurchmesser und ARG 3 entspricht der Wahl der Ungleichheit für den GDM, daher 0 für "<" und 1 für ">"


use application "common";
use application 'polytope';
use Algorithm::Combinatorics;

sub checkLatticePointsAndDiameter {
	my ($P) = shift;					#Polytop wird in P gespeichert
	my $checkLatticePoints = $ARGV[2];	
	my $checkLatticeDiameter = $ARGV[3];
	my $checkLatticeDiameterMode = $ARGV[4];

	my $PLatticePoints = $P->INTERIOR_LATTICE_POINTS;		#GitterPunkte werden ermittelt
	print "Interior lattice points of the current polytope: " . $PLatticePoints->rows . "\n";
	if (($PLatticePoints->rows != $checkLatticePoints)){
		print "Polytope refused!\n\n";
		return;
	}
	
	#Es wird eine Liste über alle möglichen 2-Kombinationen von Gitterpunkten erstellt
	my @listOfLatticePoints = (0..$PLatticePoints->rows-1);
	my $iter = Algorithm::Combinatorics::combinations(\@listOfLatticePoints, 2);
	
	#je zwei Punkte werden benutzt um eine Strecke zu erzeugen, deren Gitterpunkte dann ermittelt werden
	my $g;
	my $gLatticePoints;
	my $maxDiameter = 0;
	while (my $c = $iter->next) {
		$g=new Polytope<Rational>(POINTS=>[$PLatticePoints->row(@$c[0]), $PLatticePoints->row(@$c[1])]);
		$gLatticePoints = $g->N_LATTICE_POINTS - 1;
		if($gLatticePoints > $maxDiameter){
			$maxDiameter = $gLatticePoints;
		}
	}

	print "Lattice diameter of the current polytope: " . $maxDiameter . "\n";
	
	if (($PLatticePoints->rows == $checkLatticePoints) && ( $maxDiameter < $checkLatticeDiameter) && ($checkLatticeDiameterMode == 0)){
		print "Conditions fulfilled, here is the Polytope... \n";
		print $P->VERTICES . "\n";
	}
	elsif (($PLatticePoints->rows == $checkLatticePoints) && ( $maxDiameter > $checkLatticeDiameter) && ($checkLatticeDiameterMode == 1)){
		print "Conditions fulfilled, here is the Polytope... \n";
		print $P->VERTICES . "\n";
	}
	else{print "Polytope refused!\n\n"}
	
	
}

#Lese Polytop und Ungleichungen für Punktebereiche
my $filenamePolytope = $ARGV[0];
my $filenamePoints = $ARGV[1];

#Lese Punkte des Polytops ein
open (DATA, $filenamePolytope);
my $polytopeMatrix = new Matrix<Rational>(<DATA>);
close (DATA);

#Erzeuge Polytop aus gegebenen Ungleichungen der Form c+x_1+...x_n>=0;
open (DATA, $filenamePoints);
my $inequalities = new Matrix<Rational>(<DATA>);
close (DATA);
my $pointsPolytope = new Polytope<Rational>(INEQUALITIES=>$inequalities);
my $pointsLatticePoints = $pointsPolytope->LATTICE_POINTS;

print "There are " . $pointsPolytope->N_LATTICE_POINTS . " polytopes to be considered... \n\n";

my $p;
my $temp;
for (my $i = 0; $i < $pointsLatticePoints->rows; $i++){
	$temp = new Matrix<Rational>($polytopeMatrix);
	$temp->row($temp->rows-1) = $pointsLatticePoints->row($i);
	$p = new Polytope<Rational>(POINTS=>$temp);
	checkLatticePointsAndDiameter($p);
}





