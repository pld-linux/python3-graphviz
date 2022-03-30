#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Simple Python interface for Graphviz
Summary(pl.UTF-8):	Prosty pythonowy interfejs do Graphviza
Name:		python-graphviz
# keep 0.16.x here for python2 support
Version:	0.16
Release:	5
Epoch:		1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/graphviz/
Source0:	https://files.pythonhosted.org/packages/source/g/graphviz/graphviz-%{version}.zip
# Source0-md5:	76a73ed4821bcd993519490ec46d2061
Patch0:		%{name}-mock.patch
URL:		https://github.com/xflr6/graphviz
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock >= 2
BuildRequires:	python-pytest >= 4
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-mock >= 1.8
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 4
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-mock >= 1.8
%endif
%endif
%if %{with tests}
BuildRequires:	graphviz
%endif
%if %{with apidocs}
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

%package -n python3-graphviz
Summary:	Simple Python interface for Graphviz
Summary(pl.UTF-8):	Prosty pythonowy interfejs do Graphviza
Group:		Libraries/Python
Requires:	graphviz
Requires:	python3-modules >= 1:3.4

%description -n python3-graphviz
This package facilitates the creation and rendering of graph
descriptions in the DOT language of the Graphviz graph drawing
software from Python.

%description -n python3-graphviz -l pl.UTF-8
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
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin,pytest_mock" \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin,pytest_mock" \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
cd docs
sphinx-build-3 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-graphviz-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-graphviz-%{version}
%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' $RPM_BUILD_ROOT%{_examplesdir}/python-graphviz-%{version}/*.py
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-graphviz-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-graphviz-%{version}
%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-graphviz-%{version}/*.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%{py_sitescriptdir}/graphviz
%{py_sitescriptdir}/graphviz-%{version}-py*.egg-info
%{_examplesdir}/python-graphviz-%{version}
%endif

%if %{with python3}
%files -n python3-graphviz
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/graphviz
%{py3_sitescriptdir}/graphviz-%{version}-py*.egg-info
%{_examplesdir}/python3-graphviz-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,*.html,*.js}
%endif
