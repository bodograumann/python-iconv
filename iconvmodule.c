#include <iconv.h>
#include <Python.h>

typedef struct {
    PyObject_HEAD
    iconv_t handle;
} IconvObject;

static PyObject *error;

static PyTypeObject Iconv_Type;

PyDoc_STRVAR(iconv_open__doc__,
             "open(tocode, fromcode) -> iconv handle\n\n"
             "allocate descriptor for character set conversion"
            );

static PyObject*
py_iconv_open(PyObject* unused, PyObject* args)
{
    char *tocode, *fromcode;
    iconv_t result;
    IconvObject *self;
    if (!PyArg_ParseTuple(args, "ss", &tocode, &fromcode)) {
        return NULL;
    }
    result = iconv_open(tocode, fromcode);
    if (result == (iconv_t)(-1)) {
        PyErr_SetFromErrno(PyExc_ValueError);
        return NULL;
    }
    self = PyObject_New(IconvObject, &Iconv_Type);
    if (self == NULL) {
        iconv_close(result);
        return NULL;
    }
    self->handle = result;
    return (PyObject*)self;
}

static void
Iconv_dealloc(IconvObject *self)
{
    iconv_close(self->handle);
    PyObject_Del(self);
}

PyDoc_STRVAR(Iconv_iconv__doc__,
             "iconv(in[, outlen[, count_only]]) -> out\n\n"
             "Convert in to out. outlen is the size of the output buffer;\n"
             "it defaults to len(in)."
            );

static PyObject*
Iconv_iconv(IconvObject *self, PyObject *args, PyObject* kwargs)
{
    PyObject *inbuf_obj;
    Py_buffer inbuf_view;
    const char *inbuf;
    char *outbuf;
    size_t inbuf_size, outbuf_size, iresult;
    long int inbuf_size_int, outbuf_size_int = -1;
    int count_only = 0;
    PyObject *result;
    static char *kwarg_names[]= {
        "s",
        "outlen",
        "count_only",
        NULL
    };
    if (!PyArg_ParseTupleAndKeywords(args, kwargs,
                                     "O|lii:iconv", kwarg_names,
                                     &inbuf_obj, &outbuf_size_int, &count_only)) {
        return NULL;
    }

    if (inbuf_obj == Py_None) {
        /* None means to clear the iconv object */
        inbuf = NULL;
        inbuf_size_int = 0;
    } else if (!PyObject_CheckBuffer(inbuf_obj)) {
        PyErr_SetString(PyExc_TypeError,
                        "iconv expects byte object as first argument");
        return NULL;
    } else if (PyObject_GetBuffer(inbuf_obj, &inbuf_view, PyBUF_SIMPLE) < 0) {
        return NULL;
    } else {
        inbuf = inbuf_view.buf;
        inbuf_size_int = inbuf_view.len;
    }

    /* If no result size estimate was given, estimate that the result
       string is the same size as the input string. */
    if (outbuf_size_int == -1) {
        outbuf_size_int = inbuf_size_int;
    }
    inbuf_size = inbuf_size_int;
    if (count_only) {
        result = NULL;
        outbuf = NULL;
        outbuf_size = outbuf_size_int;
    } else {
        /* Allocate the result string. */
        result = PyBytes_FromStringAndSize(NULL, outbuf_size_int);
        if (!result) {
            return NULL;
        }
        outbuf = PyBytes_AS_STRING(result);
        outbuf_size = outbuf_size_int;
    }
    /* Perform the conversion. */
    iresult = iconv(self->handle, &inbuf, &inbuf_size, &outbuf, &outbuf_size);

    PyBuffer_Release(&inbuf_view);

    if (count_only) {
        result = PyLong_FromLong(outbuf_size_int-outbuf_size);
    } else {
        _PyBytes_Resize(&result, outbuf_size_int-outbuf_size);
    }

    if (iresult == -1) {
        PyObject *exc;
        exc = PyObject_CallFunction(error,"siiO",
                                    strerror(errno),errno,
                                    inbuf_size_int - inbuf_size,
                                    result);
        Py_DECREF(result);
        PyErr_SetObject(error,exc);
        return NULL;
    }
    return result;
}

static PyMethodDef Iconv_methods[] = {
    {   "iconv", (PyCFunction)Iconv_iconv,
        METH_KEYWORDS|METH_VARARGS, Iconv_iconv__doc__
    },
    {NULL, NULL} /* sentinel */
};

static PyTypeObject Iconv_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Iconv",
    .tp_basicsize = sizeof(IconvObject),
    .tp_dealloc = (destructor)Iconv_dealloc,
    .tp_methods = Iconv_methods,
};

static PyMethodDef iconv_methods[] = {
    {   "open", py_iconv_open,
        METH_VARARGS, iconv_open__doc__
    },
    {NULL, NULL} /* sentinel */
};

PyDoc_STRVAR(__doc__,
             "The iconv module provides an interface to the iconv library."
            );

PyMODINIT_FUNC
PyInit_iconv(void)
{
    PyObject *m, *d;

    #ifdef Py_SET_TYPE
        // Available since python 3.9, required since python 3.11
        Py_SET_TYPE(&Iconv_Type, &PyType_Type);
    #else
        // Fallback for python 3.6, 3.7 and 3.8
        Py_TYPE(&Iconv_Type) = &PyType_Type;
    #endif
    if (PyType_Ready(&Iconv_Type) < 0) {
        return NULL;
    }

    /* Create the module and add the functions */
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        .m_name = "iconv",
        .m_doc = __doc__,
        .m_size = -1,
        .m_methods = iconv_methods,
    };
    if ((m = PyModule_Create(&moduledef)) == NULL) {
        return NULL;
    }

    /* Add some symbolic constants to the module */
    d = PyModule_GetDict(m);
    error = PyErr_NewException("iconv.error", PyExc_ValueError, NULL);
    PyDict_SetItemString(d, "error", error);

    return m;
}
