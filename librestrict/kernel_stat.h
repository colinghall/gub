/* Definition of `struct stat' used in the kernel..  */
struct kernel_stat
  {
    unsigned short int st_dev;
    unsigned short int __pad1;
#define _HAVE___PAD1
    unsigned long int st_ino;
    unsigned short int st_mode;
    unsigned short int st_nlink;
    unsigned short int st_uid;
    unsigned short int st_gid;
    unsigned short int st_rdev;
    unsigned short int __pad2;
#define _HAVE___PAD2
    unsigned long int st_size;
    unsigned long int st_blksize;
    unsigned long int st_blocks;
    struct timespec st_atim;
    struct timespec st_mtim;
    struct timespec st_ctim;
    unsigned long int __unused4;
#define _HAVE___UNUSED4
    unsigned long int __unused5;
#define _HAVE___UNUSED5
  };

#define _HAVE_STAT___UNUSED4
#define _HAVE_STAT___UNUSED5
#define _HAVE_STAT___PAD1
#define _HAVE_STAT___PAD2
#define _HAVE_STAT_NSEC
#define _HAVE_STAT64___PAD1
#define _HAVE_STAT64___PAD2
# ifdef __USE_FILE_OFFSET64 /* FIXME: CONFIG? */
# define _HAVE_STAT64___ST_INO
# endif
#define _HAVE_STAT64_NSEC
