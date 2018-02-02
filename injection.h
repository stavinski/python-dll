#include <windows.h>

#ifndef CFFI_DLLIMPORT
#  if defined(_MSC_VER)
#    define CFFI_DLLIMPORT  extern __declspec(dllimport)
#  else
#    define CFFI_DLLIMPORT  extern
#  endif
#endif

CFFI_DLLIMPORT int attach(void);
CFFI_DLLIMPORT int detach(void);
