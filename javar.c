#include "unistd.h"
#include "Python.h"

#ifndef MAXPATH
const int MAXPATH=1024;
#endif

int main(int argc, char* argv[]) {
    int i;
    char path[MAXPATH];
    getcwd(path, MAXPATH);

    // start python
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/etc/javareflect/')");

    PyObject* pModule = PyImport_ImportModule("handleMain");
    if (!pModule) {
        printf("Can not find handleMain.py file.\n");
        exit(1);
    }

    PyObject* pFunc = PyObject_GetAttrString(pModule, "main");
    PyObject* pArgs = PyTuple_New(argc+1);

    PyTuple_SetItem(pArgs, 0, Py_BuildValue("s", path));
    
    for (i=0; i<argc; i++) {
        PyTuple_SetItem(pArgs, i+1, Py_BuildValue("s", argv[i]));
    }

    PyEval_CallObject(pFunc, pArgs);
    Py_Finalize();

    exit(0);
}












