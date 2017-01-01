#ifndef FLANDERS_H_INCLUDED
#define FLANDERS_H_INCLUDED

#ifndef FLANDERS_API
#  ifdef _WIN32
#    if defined(FLANDERS_BUILD_SHARED) /* build dll */
#      define FLANDERS_API __declspec(dllexport)
#    elif !defined(FLANDERS_BUILD_STATIC) /* use dll */
#      define FLANDERS_API __declspec(dllimport)
#    else /* static library */
#      define FLANDERS_API
#    endif
#  else
#    if __GNUC__ >= 4
#      define FLANDERS_API __attribute__((visibility("default")))
#    else
#      define FLANDERS_API
#    endif
#  endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

FLANDERS_API int foo(const int i);

#ifdef __cplusplus
}
#endif

#endif /* FLANDERS_H_INCLUDED */
