#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Simple Python interface for Graphviz
Summary(pl.UTF-8):	Prosty pythonowy interfejs do Graphviza
Name:		python-graphviz
Version:	0.20.3
Release:	1
Epoch:		1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/graphviz/
Source0:	https://files.pythonhosted.org/packages/source/g/graphviz/graphviz-%{version}.zip
# Source0-md5:	b7c6caf06c0badc770b187645519ea28
URL:		https://github.com/xflr6/graphviz
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 4
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-mock >= 1.8
%endif
%if %{with tests}
BuildRequires:	graphviz
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.7
%endif
Requires:	graphviz
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package facilitates the creation and rendering of graph
descriptions in the DOT language of the Graphviz graph drawing
software from Python.

%description -l pl.UTF-8
Ten pakiet wspomaga tworzenie i renderowanie opisów grafów w języku
DOT oprogramowania do rysowania grafów Graphviz z poziomu Pythona.

%package apidocs
Summary:	API documentation for Python graphviz module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona graphviz
Group:		Documentation

%description apidocs
API documentation for Python graphviz module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona graphviz.

%prep
%setup -q -n graphviz-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin,pytest_mock" \
%{__python3} -m pytest tests/backend
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-graphviz-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-graphviz-%{version}
%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-graphviz-%{version}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/graphviz
%{py3_sitescriptdir}/graphviz-%{version}-py*.egg-info
%{_examplesdir}/python3-graphviz-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,*.html,*.js}
%endif
