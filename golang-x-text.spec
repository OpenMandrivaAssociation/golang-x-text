%global debug_package %{nil}

%bcond_without bootstrap2

# Run tests in check section
%bcond_without check

# https://github.com/golang/net
%global goipath		golang.org/x/text
%global forgeurl	https://github.com/golang/text
Version:		0.14.0

%gometa

Summary:	Go text processing support	
Name:		golang-x-text

Release:	1
Source0:	https://github.com/golang/text/archive/v%{version}/text-%{version}.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golang-package-dependencies.sh
%endif
URL:		https://github.com/golang/text
License:	BSD with advertising
Group:		Development/Other
BuildRequires:	compiler(go-compiler)

%description
This package provides supplementary Go libraries
for text processing, many involving Unicode.

%files
%license LICENSE
%doc README.md
%{_bindir}/gotext

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n text-%{version}

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

%build
%gobuildroot
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done


%check
%if %{with check}
%gochecks
%endif

