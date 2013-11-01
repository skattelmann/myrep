//INPUT: Eine Liste (den Pfadnamen) mit Polytopen, die ausschliesslich echte Ecken besitzen. 
//OUTPUT: Eine Liste "newPolytopes.txt", die alle Polytope der ursprünglichen Liste modulo Unimodularität und Translation beinhaltet

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import org.jblas.DoubleMatrix;
import Jama.Matrix;

public class unimodularityCheck {

	
	public static void main(String[] args) throws IOException {
		
		// für die Zeit
		long start = System.currentTimeMillis();
		
		String filename = args[0];
		BufferedReader input = new BufferedReader( new FileReader( filename ) );
		
		ArrayList<DoubleMatrix> polytopes = new ArrayList<DoubleMatrix>();
		
		// Einlesen der Liste von Polytope
		System.out.println("Lese Polytope ein ...");
		while( input.ready() ){
			
			polytopes.add( new DoubleMatrix( Matrix.read(input).getArray() ));
			
		}
		System.out.println("Einlesen beendet.\nAnzahl der Polytope: " + polytopes.size() + "\n");
		input.close();
		
		// Erster Schritt: Prüfe auf gleiche Polytope
		System.out.println("Starte Test auf Gleichheit ...");
		for (int i = 0; i < polytopes.size(); i++) {
			   for(int j = i+1; j < polytopes.size(); j++){
				   
				  if( polytopes.get(i).equals(polytopes.get(j)) ){
					  polytopes.remove(j);
				  }
				   
			   }
		}
		System.out.println("Verbleibende Polytope: " + polytopes.size() + "\n");
		
		
		// Zweiter Schritt: Berechne mögliche lineare Abbildungen und teste, ob |det (L)| = 1
		System.out.println("Starte Test auf Unimodularität ...");
		DoubleMatrix tempPolytopeA, tempPolytopeB;
		DoubleMatrix previousVertexA, nextVertexA, previousVertexB, nextVertexB;
		Matrix solutionA_JAMA, solutionB_JAMA;
		
		Matrix L_JAMA; 			// hier werden mögliche unimodulare Abbildungen gespeichert
		DoubleMatrix L_JBLAS;	// es müssen leider Methoden von JAMA UND JBLAS benutzt werden...
		
		int s;
		
		DoubleMatrix currentPolytope;
		DoubleMatrix toBeCheckedAgainstCurrentPolytope;
		
		boolean flagForChecked = false;
		
		for (int k = 0; k < polytopes.size(); k++){
			
			currentPolytope = polytopes.get(k);
			
			for(int l = 0; l < currentPolytope.rows; l++){
				
				// Verschiebe in den Ursprung und bilde die Nachbarecken für das erste Polytop ...
				tempPolytopeA = currentPolytope.dup();
				tempPolytopeA = tempPolytopeA.subRowVector(currentPolytope.getRow(l));
				
				
				if( l > 0){
					previousVertexA = tempPolytopeA.getRow(l-1);
				}
				else{
					previousVertexA = tempPolytopeA.getRow(tempPolytopeA.getRows() - 1);
				}
				
				
				if( l < tempPolytopeA.rows - 1){
					nextVertexA = tempPolytopeA.getRow(l+1);
				}
				else{
					nextVertexA = tempPolytopeA.getRow(0);
				}
				
				
				// ... dann das gleiche nochmal für das zweite Polytop
				for (int m = k+1; m < polytopes.size(); m++){

					toBeCheckedAgainstCurrentPolytope = polytopes.get(m);
					
					// wenn beide Polytope eine ungleiche Zahl von Ecken haben können sie nicht unimodular äquivalent sein
					if(currentPolytope.rows != toBeCheckedAgainstCurrentPolytope.rows) continue;
					
					tempPolytopeB = toBeCheckedAgainstCurrentPolytope.dup();
					
					flagForChecked = false;
					
					for(int n = 1; n < toBeCheckedAgainstCurrentPolytope.rows; n++){	
						
						if (flagForChecked == true) { 
							//NEU: counter muss um 1 zurückgesetzt werden wenn die Liste gekürzt wird
							m = m - 1;
							break; 	
						}
						
						tempPolytopeB = tempPolytopeB.subRowVector(toBeCheckedAgainstCurrentPolytope.getRow(n));
						
						previousVertexB = tempPolytopeB.getRow(n-1);
						if( n < tempPolytopeB.rows - 1){
							nextVertexB = tempPolytopeB.getRow(n+1);
						}
						else{
							nextVertexB = tempPolytopeB.getRow(0);
						}

						// ab hier beginnt das eigentliche Prüfen auf Unimodularität
						// Ecken werden bei JAMA als ROWS und bei JBLAS als COLS in die Matrizen eingetragen
						solutionA_JAMA = new Matrix( new double[][] { previousVertexA.getRow(0).toArray(), nextVertexA.getRow(0).toArray() } );
						solutionB_JAMA = new Matrix( new double[][] { previousVertexB.getRow(0).toArray(), nextVertexB.getRow(0).toArray() } );
						
						L_JAMA = solutionB_JAMA.transpose().times(solutionA_JAMA.transpose().inverse());
						L_JBLAS = new DoubleMatrix( L_JAMA.getArray() );
						
						if( checkForIntegrality(L_JBLAS) && Math.abs(L_JAMA.det()) == 1.0 ){
							
								// 'rechtsherum' prüfen
								for (s = 0; s < tempPolytopeA.rows; s++) {
							
									if( !L_JBLAS.mmul(tempPolytopeA.getRow( (l+s)%tempPolytopeA.rows ).transpose()).equals(tempPolytopeB.getRow( (n+s)%tempPolytopeB.rows ).transpose()) ){
											
										break;
																							
									}
													
								}
										
								if( s == tempPolytopeA.rows ){ 
									
									flagForChecked = true;
									polytopes.remove(m); 
									
								}

						}
						
						// und die andere Variante ...
						solutionA_JAMA = new Matrix( new double[][] { previousVertexA.getRow(0).toArray(), nextVertexA.getRow(0).toArray() } );
						solutionB_JAMA = new Matrix( new double[][] { nextVertexB.getRow(0).toArray(), previousVertexB.getRow(0).toArray() } );
						L_JAMA = solutionB_JAMA.transpose().times(solutionA_JAMA.transpose().inverse());
						L_JBLAS = new DoubleMatrix( L_JAMA.getArray() );
						
												
						if( flagForChecked == false && checkForIntegrality(L_JBLAS) && Math.abs(L_JAMA.det()) == 1.0 ){
							
								// 'über Kreuz' prüfen
								for (s = 0; s < tempPolytopeA.rows; s++) {
									
									if( !L_JBLAS.mmul(tempPolytopeA.getRow( (l+s)%tempPolytopeA.rows ).transpose()).equals(tempPolytopeB.getRow( (n-s+tempPolytopeB.rows)%tempPolytopeB.rows ).transpose()) ){
											
										break;
																							
									}
													
								}
										
								if( s == tempPolytopeA.rows ){ 
									
									flagForChecked = true;
									polytopes.remove(m); 
								
								}

						}
						
					}
				}
			}
		}
		
		System.out.println("Neue Anzahl der Polytope: " + polytopes.size());
		
		// schreibe übrige Polytope in eine neue Text-Datei
		FileWriter out = new FileWriter("newPolytopes.txt");
		for (DoubleMatrix polytopeToBeWritten : polytopes) {
			
			for (int i = 0; i < polytopeToBeWritten.rows; i++) {
				
				for (int j = 0; j < 2; j++) {
					
					out.write( ((int) polytopeToBeWritten.get(i, j)) + " ");
					
				}
				
				out.write("\n");
				
			}
			
			out.write("\n");
			
		}
		
		out.close();
			
		long end = System.currentTimeMillis();

		System.out.println("\nBenötigte Zeit: " + (end-start) + " ms.");
		
	}
	
	
	

	private static boolean checkForIntegrality(DoubleMatrix l_JBLAS) {
		
		//Hier kann die Genauigkeit für die Ganzzahligkeit eingestellt werden
		double limit = 0.000001;
		
		if( (Math.abs(l_JBLAS.get(0, 0)%1) < limit)
			&& (Math.abs(l_JBLAS.get(0, 1)%1) < limit)
			&& (Math.abs(l_JBLAS.get(1, 0)%1) < limit)
			&& (Math.abs(l_JBLAS.get(1, 1)%1) < limit) ){
			return true;
			
		}
		
		return false;
		
	}

}
