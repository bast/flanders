#ifndef CPP_INTERFACE_H_INCLUDED
#define CPP_INTERFACE_H_INCLUDED

#ifndef CPP_INTERFACE_API
#  ifdef _WIN32
#    if defined(CPP_INTERFACE_BUILD_SHARED) /* build dll */
#      define CPP_INTERFACE_API __declspec(dllexport)
#    elif !defined(CPP_INTERFACE_BUILD_STATIC) /* use dll */
#      define CPP_INTERFACE_API __declspec(dllimport)
#    else /* static library */
#      define CPP_INTERFACE_API
#    endif
#  else
#    if __GNUC__ >= 4
#      define CPP_INTERFACE_API __attribute__((visibility("default")))
#    else
#      define CPP_INTERFACE_API
#    endif
#  endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

CPP_INTERFACE_API int foo(const int i);

#ifdef __cplusplus
}
#endif

#endif /* CPP_INTERFACE_H_INCLUDED */
