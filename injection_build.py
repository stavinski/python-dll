import cffi

ffibuilder = cffi.FFI()

with open("injection.h") as f:
  data = "".join([line for line in f if not line.startswith("#")])
  data = data.replace('CFFI_DLLIMPORT', '')
  ffibuilder.embedding_api(data)
  
ffibuilder.set_source("injection", r'''
    #include "injection.h"
          
    BOOL APIENTRY DllMain(HINSTANCE hInstDll, DWORD fdwReason, LPVOID lpvReserved)
    {
        switch (fdwReason)
        {
            case DLL_PROCESS_ATTACH:
                return attach();
            case DLL_PROCESS_DETACH:
                return detach();
            default:
                // do nothing
                break;
        }
        
        return TRUE;
    }
''')

ffibuilder.embedding_init_code("""
    from injection import ffi, lib
    import ctypes

    @ffi.def_extern()
    def attach():
        MessageBox = ctypes.windll.user32.MessageBoxA
        MessageBox(None, 'attach', 'Window title', 0)

        return 0
        
    @ffi.def_extern()
    def detach():
        MessageBox = ctypes.windll.user32.MessageBoxA
        MessageBox(None, 'detach', 'Window title', 0)

        return 0
""")

ffibuilder.compile(target="injection-1.0.*", verbose=True)