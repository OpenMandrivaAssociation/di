%define major 6
%define libname %mklibname di
%define devname %mklibname di -d
# tests complete satisfactory in vm, disable for ABF/CI building
%bcond tests 0

Name:		di
Version:	6.2.2.2
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
BuildRequires:	glibc-devel
BuildRequires:	gettext
BuildRequires:	grep
BuildRequires:	intltool
BuildRequires:	ninja
BuildRequires:	pkgconfig
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
Group:		System/Libraries
%rename libdi6

%description -n %{libname}
di (libdi) is a disk information utility library

%package -n %{devname}
Summary:	Development files for the di disk information utility library
Group:	Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files for the %{libname} disk information utility library.

%prep
%autosetup -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%ldflags"
%cmake	\
	-DCMAKE_BUILD_TYPE=Release \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# set executable bit on example build script
chmod +x %{buildroot}%{_datadir}/%{name}/examples/build.sh
%find_lang %{name}
# compress man pages
zstd -r --rm man/*di.3

%if %{with tests}
%check
%ninja -v -C build ditest
%endif

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.md
%license LICENSE.txt
%{_bindir}/%{name}
%{_mandir}/man1/di.1.zst

%files -n %{libname}
%doc README.md
%{_libdir}/lib%{name}.so.%{major}{,.*}

%files -n %{devname}
%license LICENSE.txt
%{_datadir}/%{name}/examples
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/di.pc
%{_mandir}/man3/libdi.3.zst
