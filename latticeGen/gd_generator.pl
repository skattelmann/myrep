#INPUT:  Gesuchter Gitterdurchmesser k
#OUTPUT: "Fast" alle Polytope mit Gitterdurchmesser k. Leider enthaelt die Liste nur alle Polytope, die in (verzerrte) ganzzahlige Rechtecke der Hoehe k und Breite k+1 (dabei ist k = Anzahl Gitterpunkte) passen.
#	 Die angegebenen Polytope haben ausschliesslich ECHTE Ecken und können deshalb mit "unimodularityCheck" weiter auf Unimodularität untersucht werden.
#	 Die Ausgabedatei heisst standardmaessig "polytopes.txt"

#Prinzipielle Arbeitsweise des Algorithmus: 
#Innerhalb einer Schablone werden (verzerrte) Rechtecke gebildet, in denen über ein Backtracking-Verfahren die Polytope gebildet werden.

use application 'polytope';
use List::MoreUtils;
use POSIX qw(ceil);
use POSIX qw(floor);

my $k = shift;			
my $boxModelMatrix;
my $boxModelPolytope;
my $boxMatrix;
my @boxMatrixArray;
my $boxMatrixLatticePoints;
my $box;

my @polytopeCollection;
my $polytopeCounter = 0;

my $latticePointsOfTheLeftLine;
my $latticePointsOfTheRightLine;

my @usedPoints = ();
my @necessaryPoints;

my $flagHasNoNewPoint;

my $i;
my $j;

#Textfile, in das die Polytope geschrieben werden
open (MYFILE, '>polytopes.txt');

########################################################################################################
########################################################################################################
#BEGINN DER HAUPTSCHLEIFE
#PRO SCHLEIFENDURCHGANG WERDEN INNERHALB EINER BOX ALLE POLYTOPE MIT GITTERDURCHMESSER K GENERIERT

for ($i = 0; $i < $k; $i++){
	
	$boxModelMatrix = new Matrix<Integer>([ [1,-$i,-$k],[1,$i,$k],[1,$k+1+$i,$k],[1,$k+1-$i,-$k] ]);
	$boxModelPolytope = new Polytope(POINTS=>$boxModelMatrix);
	
	$boxMatrixLatticePoints = $boxModelPolytope->LATTICE_POINTS;
		
	$latticePointsOfTheLeftLine = new Polytope(POINTS=>[ [1,-$i,-$k],[1,$i,$k] ])->LATTICE_POINTS;
	$latticePointsOfTheRightLine = new Polytope(POINTS=>[ [1,$k+1+$i,$k],[1,$k+1-$i,-$k] ] )->LATTICE_POINTS;
	
	@necessaryPoints = ();
	
	for(my $l = 0; $l < $boxMatrixLatticePoints->rows; $l++){
		if( grep { $_ ==  $boxMatrixLatticePoints->row($l) } @usedPoints ) { next }
		else{ push( @necessaryPoints, $boxMatrixLatticePoints->row($l) ) }
	}
	
	print "+++++\nANZAHL NEUER PUNKTE: " . ($#necessaryPoints + 1) . "\n";
	
	for ($j = 0; $j <= floor($k/2); $j++){	

		print "Bearbeitung von Box " . (($i*(floor($k/2)+1))+($j+1)) . " von " . ( $k * (floor($k/2)+1) ) . " ... \n";

		@boxMatrixArray = ();
		$flagHasNoNewPoint = 1;
		for(my $l = 0; $l < $boxMatrixLatticePoints->rows; $l++){
			if( $boxMatrixLatticePoints->($l, 2) >= -$j && $boxMatrixLatticePoints->($l, 2) <= $k-$j ){
				push( @boxMatrixArray, $boxMatrixLatticePoints->row($l) );
				#prüfe, ob überhaupt ein neuer Punkt in der neuen Box enhalten ist
				if( grep { $_ == $boxMatrixLatticePoints->row($l) } @necessaryPoints ){ $flagHasNoNewPoint = 0 }	
			}
		}
		
		if( $flagHasNoNewPoint == 1 ){ next }  #wenn in der neuen Box keine neuen Punkte enthalten sind ist nicht zu machen
		
		$boxMatrix = new Matrix<Int>(@boxMatrixArray);
		$box = new Polytope(POINTS=>$boxMatrix);
		
		#generate possible Polytopes
		generatePolytopes($box);
		
	}
	
	@usedPoints = @$boxMatrixLatticePoints;

}

 close (MYFILE); 

print "Es wurden ";
print $polytopeCounter;
print " Polytope gefunden!\n";

#ENDE DER HAUPTSCHLEIFE
########################################################################################################
########################################################################################################


#Ausgangsmethode für das Generieren der Polytope
sub generatePolytopes{
	
	my $currentBox = shift;					
	my $currentBoxPoints = $currentBox->LATTICE_POINTS;
	
	my @startPoints = generateStartPoints($currentBoxPoints);
	
	print "ANZAHL STARTPUNKTE: " . @startPoints . "\n";
	sleep 1;

	foreach my $startPoint (@startPoints) {
		backtrackPolytopeLine( [$startPoint], [0] ,$currentBoxPoints);  #0 nur für Initialisierung
	}
	
}


#Startpunkte für das Backtracking werden generiert
sub generateStartPoints{
	
	my $currentBoxPoints = shift;	
	my $currentLowerLeftBoxPoint = $currentBoxPoints->row(0);
	my $leftBoundOfLatticeDiameter = new Vector<Integer>([1,1,0]);
	my @startPoints;
	
	#Der "linke" Punkt der Strecke, die den Gitterdurchmesser repräsentiert, ist stets ein Startpunkt
	push(@startPoints, $leftBoundOfLatticeDiameter);		
	
	#Die "Standardboxen" benötigen nur einen Startpunkt, s.o.
	if( @$currentLowerLeftBoxPoint[1] == 0 && @$currentLowerLeftBoxPoint[2] == 0 ){
		return @startPoints;
	}
	
	#sonst suche alle gültigen Startpunkte zusammen. Diese können (bis auf den obigen Startpunkt) nur aus dem oberen Bereich der Schablone kommen
	foreach my $point (@$currentBoxPoints){
		if( @$point[2] > 0 && @$point[2] > @$point[1] - 1 ){
				push(@startPoints, $point);
		}	
	}
	
	return @startPoints;
	
}


#Das eigentliche Backtracking-Verfahren
sub backtrackPolytopeLine{
	
	my ($currentPolytopeList, $newPoint, $currentBoxPoints) = @_;
	my @newPolytopeList = @$currentPolytopeList;
	my $sizeOfNewPolytope = @newPolytopeList;
	my $orthVector;
	
	#Für den Start
	if(@$newPoint[0] != 0){
		
		push(@newPolytopeList, $newPoint);
		$sizeOfNewPolytope = @newPolytopeList;

		#Teste Spezialfall: Zwei Punkte auf jeweils linken und rechten Rand der Box auf gleicher Höhe würde eine Überschreitung des Gitterdurchmessers bedeuten
		for( my $l = 0; $l < $sizeOfNewPolytope - 1; $l++){
			
			if( abs( $newPolytopeList[$sizeOfNewPolytope-1][1] - $newPolytopeList[$l][1] ) > $k ){ 
				
				#liegt auf gleicher Achse
				if( $newPolytopeList[$sizeOfNewPolytope-1][2] == $newPolytopeList[$l][2] ){ return }
				
				
				if (grep {$_ == $newPolytopeList[$sizeOfNewPolytope-1]} @$latticePointsOfTheRightLine) {
						if (grep {$_ == $newPolytopeList[$l] && abs(@$_[2]) < abs($newPolytopeList[$sizeOfNewPolytope-1][2]) } @$latticePointsOfTheLeftLine 
							&& grep {$_ == $newPolytopeList[$l+1] && abs(@$_[2]) > abs($newPolytopeList[$sizeOfNewPolytope-1][2]) } @$latticePointsOfTheLeftLine) {
							
							return; #DURCHMESSER ÜBERSCHRITTEN
							
						}
					}
				
					
				if (grep {$_ == $newPolytopeList[$sizeOfNewPolytope-1]} @$latticePointsOfTheLeftLine) {
						if (grep {$_ == $newPolytopeList[$l] && abs(@$_[2]) < abs($newPolytopeList[$sizeOfNewPolytope-1][2]) } @$latticePointsOfTheRightLine 
							&& grep {$_ == $newPolytopeList[$l+1] && abs(@$_[2]) > abs($newPolytopeList[$sizeOfNewPolytope-1][2]) } @$latticePointsOfTheRightLine) {
							
							return; #DURCHMESSER ÜBERSCHRITTEN
							
						}
					}
					
				}
		}

		#Hier werden zahlreiche Kriterien, denen ein generiertes Polytop genügen muss, abgeprüft.
		#-Das Polytop muss geschlossen sein (Abschluss findet von unten nach oben statt)
		#-Konvexität
		#-es muss ein noch nicht benutzter Punkt im Polytop liegen (aus diesem Grund sind alle generierten Polytope paarweise verschieden modulo Translation + Unimodularität)
		#-die letzten beiden Punkte dürfen sich nicht gleichzeitig auf dem linken Rand der Box befinden (sonst wird der Gitterdurchmesser um 1 überschritten)
		if($newPolytopeList[$sizeOfNewPolytope-1] == $newPolytopeList[0] && (($newPolytopeList[$sizeOfNewPolytope-2][2] < 0 
			&& $newPolytopeList[$sizeOfNewPolytope-1][2] > 0) || ($newPolytopeList[$sizeOfNewPolytope-1][1] == 1 && $newPolytopeList[$sizeOfNewPolytope-1][2] == 0)) 
				&& ( not (grep { $_ == $newPolytopeList[0] } @$latticePointsOfTheLeftLine) || not (grep { $_ == $newPolytopeList[$sizeOfNewPolytope-2] } @$latticePointsOfTheLeftLine ) ) 
				){
			
			#Prüfe, ob Abscluss wirklich von unten nach oben stattfindet
			if( $j > 0 && not grep { $$_[2] == -$j } @newPolytopeList  )	{ return }
			
			#teste ob Startpukt auf Linie zwischen dem ersten und letzten Punkt liegt (dann wäre der Startpunkt keine echte Ecke mehr)
			if( dotProduct( $newPolytopeList[$sizeOfNewPolytope-2] - $newPolytopeList[0] , getOrthogonalVector( $newPolytopeList[1] , $newPolytopeList[0] ) ) >= 0){ return }
				
			foreach my $point ( @newPolytopeList ){

				#wenn ein neuer Punkt im Polytop enthalten ist wird es geprintet
				if ( grep {$_ == $point} @necessaryPoints ){
					
					#letzter Punkt ist gleichzeitig der Startpunkt und kann gelöscht werden
					pop(@newPolytopeList);
									
					foreach my $point2 ( @newPolytopeList ){print MYFILE @$point2[1] . " " . @$point2[2] . "\n"}
					print MYFILE "\n";
								
					$polytopeCounter += 1;
			
					return;
			
				}
			}
		}
		
		#ein Übergang zu y > 0 kann nur stattfinden wenn der Startpunkt gefunden wurde
		if($newPolytopeList[$sizeOfNewPolytope-2][2] < 0 && $newPolytopeList[$sizeOfNewPolytope-1][2] > 0 ){
			return;
		}
		
		#bilde orthogonalen Vektor für spätere Betrachtungen
		$orthVector = getOrthogonalVector($newPolytopeList[$sizeOfNewPolytope-1], $newPolytopeList[$sizeOfNewPolytope-2]);
			
	}
	

	#versuche mit allen "möglichen" Richtungen fortzufahren
	#Dabei wird überprüft ob die Konvexität erhalten bleibt
	for(my $i = 0; $i < $currentBoxPoints->rows; $i++){
		
		#Fall Startpunkt (daher kein neuer Punkt und die Länge der bisherigen Liste ist 1)
		if($sizeOfNewPolytope == 1){
			if($currentBoxPoints->($i,2) > 0){ 
				backtrackPolytopeLine(\@newPolytopeList, $currentBoxPoints->row($i), $currentBoxPoints); 
			}
			else{ next }
		}
		#Fall neuer Punkt kommt von oberer Halbebene
		elsif( $newPolytopeList[$sizeOfNewPolytope-1][2] > 0){			
			if( ( dotProduct($orthVector, $currentBoxPoints->row($i) - $newPolytopeList[$sizeOfNewPolytope-1]) < 0 )	#bleibt Konvexität erhalten?
				&& (($currentBoxPoints->($i,1) - $newPolytopeList[$sizeOfNewPolytope-1][1])*($newPolytopeList[$sizeOfNewPolytope-1][2])+($currentBoxPoints->($i,2) - $newPolytopeList[$sizeOfNewPolytope-1][2])*($k+1-$newPolytopeList[$sizeOfNewPolytope-1][1]) >= 0) 
					&& ( dotProduct( $currentBoxPoints->row($i) - $newPolytopeList[0] , getOrthogonalVector( $newPolytopeList[1] , $newPolytopeList[0] ) ) <= 0) ){
					backtrackPolytopeLine(\@newPolytopeList, $currentBoxPoints->row($i), $currentBoxPoints);
			}
		}
		#Fall neuer Punkt kommt von unterer Halbebene oder rechter Rand vom Durchmesser
		elsif( ($newPolytopeList[$sizeOfNewPolytope-1][2] < 0 || $newPolytopeList[$sizeOfNewPolytope-1][1] == $k+1)){		
			if( ( dotProduct($orthVector, $currentBoxPoints->row($i) - $newPolytopeList[$sizeOfNewPolytope-1]) < 0 )	#bleibt Konvexität erhalten?
				&& (($currentBoxPoints->($i,1) - $newPolytopeList[$sizeOfNewPolytope-1][1])*($newPolytopeList[$sizeOfNewPolytope-1][2])+($currentBoxPoints->($i,2) - $newPolytopeList[$sizeOfNewPolytope-1][2])*(1-$newPolytopeList[$sizeOfNewPolytope-1][1]) >= 0)
					&& ( dotProduct( $currentBoxPoints->row($i) - $newPolytopeList[0] , getOrthogonalVector( $newPolytopeList[1] , $newPolytopeList[0] ) ) <= 0) ){
					backtrackPolytopeLine(\@newPolytopeList, $currentBoxPoints->row($i), $currentBoxPoints);
			}
		}		
	}

	return;

}


sub getOrthogonalVector{
	my ( $a, $b ) = @_;
	my $orthVector = new Vector<Rational>( [ 1, @$b[2]-@$a[2], @$a[1]-@$b[1] ] );
	return $orthVector;
}

sub dotProduct{
	my ($a, $b) = @_;
	return ( @$a[1] * @$b[1] + @$a[2] * @$b[2] );
}



