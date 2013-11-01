/**
 *\ @file timer.c
 * @brief Wall and CPU time function 
 * @author Martin Köhler
 *
 * This file implelemts a function to get the wall-time and the cpu time. 
 */

#include <stdio.h> 
#include <unistd.h>
#include <sys/time.h>
#include <stdint.h>
#include <time.h>
#include "timer.h"
/** 
 * @brief Get the current time of day for measurement purpose 
 * @return a double value with the enlapsed time in seconds 
 *
 * The walltime function can be used for easy runtime measuring. It returns a time as a double. 
 * The time measuring will work like the following: 
 * \code
 *  double tStart, tEnd, tRun; 
 *  tStart = walltime(); 
 *  doSomething(); 
 *  tEnd = walltime(); 
 *  tRun = tEnd-tStart; 
 * \endcode
 *
 */
double walltime()
{
	struct timeval tv;
	gettimeofday (&tv, NULL);
	return tv.tv_sec + tv.tv_usec / 1e6;
}
double walltime_(){
	return walltime(); 
}


/** 
 * @brief get the current CPU time  
 * @return a double value containing the enlasped CPU time.  
 * 
 * The cputime function can be used for easy CPU time measuring. It returns a time as a double. 
 * The time measuring will work like the following: 
 * \code
 *  double tStart, tEnd, tRun; 
 *  tStart = cputime(); 
 *  doSomething(); 
 *  tEnd = cputime(); 
 *  tRun = tEnd-tStart; 
 * \endcode
 */
double cputime() {
	clock_t  t = clock(); 
	return t / (double)(CLOCKS_PER_SEC); 
}

double cputime_() {
	return cputime(); 
}
