#include <stdio.h>
#include <stdlib.h>
#include "casadi_bug_fun.c"

int main() {
  int sz_arg, sz_res, sz_iw, sz_w;
  casadi_bug_fun_work(&sz_arg, &sz_res, &sz_iw, &sz_w);
  
  // allocate work vectors and IO buffers
  const double **arg = calloc(sz_arg, sizeof(double*));
  double **res = calloc(sz_res, sizeof(double*));
  int *iw = calloc(sz_iw, sizeof(int));
  double *w = calloc(sz_w, sizeof(double));

  // set up input/output buffers
  double input0 = 0.0;
  double output0[1000]; // big enough
  arg[0] = &input0;
  res[0] = output0;

  // call the function
  const int mem = 0;  // what is this??

  // first call
  casadi_bug_fun(arg, res, iw, w, mem);
  // print outputs from first call
  printf("first c call:       ");
  for (int k=0; k<5; k++) {
    printf("%.2f, ", output0[k]);
  }
  printf("\n");

  // second call
  casadi_bug_fun(arg, res, iw, w, mem);
  // print outputs from second call
  printf("second c call:      ");
  for (int k=0; k<5; k++) {
    printf("%.2f, ", output0[k]);
  }
  printf("\n");

  // third call
  casadi_bug_fun(arg, res, iw, w, mem);
  // print outputs from third call
  printf("third c call:       ");
  for (int k=0; k<5; k++) {
    printf("%.2f, ", output0[k]);
  }
  printf("\n");

  return 0;
}
