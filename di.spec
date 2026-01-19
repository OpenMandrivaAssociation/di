%define major 6
%define libname lib%{name}%{major}
%define devname %mklibname di -d

# NOTE	di has no builtin cmake tests, skipped %%check

Name:		di
Version:	6.2.1
Release:	1
Summary:	Disk Information utility
URL:		https://diskinfo-di.sourceforge.io/
License:	Zlib
Group:		System/Utilities
Source0:	https://sourceforge.net/projects/diskinfo-di/files/%{name}-%{version}.tar.gz

BuildRequires:	bash
BuildRequires:	cmake
BuildRequires:	coreutils
BuildRequires:	gawk
BuildRequires:	gettext
BuildRequires:	grep
BuildRequires:	intltool
BuildRequires:	ninja
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(libtommath)
BuildRequires:	sed

%description
'di' is a disk information utility, displaying everything (and more) that
your 'df' command does.

It features the ability to display your disk usage in
whatever format you prefer. It is designed to be highly portable.

Great for heterogenous networks.

%package -n %{libname}
Summary:	Disk Information Utility shared library

%description -n %{libname}
di (libdi) is a disk information utility library

%package -n %{devname}
Summary: Development files for the di disk information utility library

%description -n %{devname}
Development files for the %{libname} disk information utility library.


%prep
%autosetup -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%ldflags"
%cmake	-DCMAKE_BUILD_TYPE=Release \
	-G Ninja
%ninja_build

%install
cd build
%ninja_install
cd ..

%find_lang %{name}
# compress man pages
zstd -r --rm man/*di.3


%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%doc README.md
%license LICENSE.txt
%{_mandir}/man1/di.1.zst
%{_bindir}/di

%files -n %{libname}
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.so.%{major}*
%doc README.md
%license LICENSE.txt

%files -n %{devname}
%{_includedir}/di.h
%{_libdir}/libdi.so
%{_libdir}/pkgconfig/di.pc
%{_mandir}/man3/libdi.3.zst
%license LICENSE.txt
