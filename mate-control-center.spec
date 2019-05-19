%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	major	1
%define	libname	%mklibname mate-window-settings %{major}
%define devname %mklibname -d mate-window-settings

%define	slabmaj	0
%define	libslab	%mklibname mate-slab %{slabmaj}
%define	devslab	%mklibname -d mate-slab

Summary:	MATE control center
Name:		mate-control-center
Version:	1.22.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		https://mate-desktop.org
Source0:	https://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	shared-mime-info
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
#BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(libcanberra-gtk3)
#BuildRequires:	pkgconfig(libebook-1.2)
BuildRequires:	pkgconfig(libmarco-private)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(libmatekbd)
BuildRequires:	pkgconfig(libmatekbdui)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(mate-settings-daemon)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
#BuildRequires:	pkgconfig(unique-3.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(xft)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	yelp-tools

Requires:	gnome-keyring
Requires:	gsettings-desktop-schemas
Requires:	mate-settings-daemon
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	shared-mime-info

%description
The MATE Desktop Environment is the continuation of GNOME 2. It provides an
intuitive and attractive desktop environment using traditional metaphors for
Linux and other Unix-like operating systems.

MATE is under active development to add support for new technologies while
preserving a traditional desktop experience.

The control center is MATE's main interface for configuration of various
aspects of your desktop.

%files -f %{name}.lang
%doc AUTHORS NEWS README COPYING
%{_sysconfdir}/xdg/menus/matecc.menu
%{_bindir}/mate-*
%{_sbindir}/mate-*
%{_libdir}/window-manager-settings/libmarco.so
%{_datadir}/applications/*
%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/glib-2.0/schemas/org.mate.control-center.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.control-center.keybinding.gschema.xml
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/mate-control-center
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_mandir}/man1/mate-*.1*

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for MATE control center
Group:		System/Libraries

%description -n %{libname}
This package contains the shared libraries used by %{name}.

%files -n %{libname}
%{_libdir}/libmate-window-settings.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries, include files for MATE control center
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains libraries and includes files for developing programs
based on %{name}.

%files -n %{devname}
%dir %{_includedir}/mate-window-settings-2.0
%{_includedir}/mate-window-settings-2.0/*
%{_libdir}/libmate-window-settings.so
%{_libdir}/pkgconfig/mate-default-applications.pc
%{_libdir}/pkgconfig/mate-keybindings.pc
%{_libdir}/pkgconfig/mate-window-settings-2.0.pc

#---------------------------------------------------------------------------

%package -n %{libslab}
Summary:	Shared library for MATE control center
Group:		System/Libraries

%description -n %{libslab}
This package contains the shared libraries used by %{name}.

%files -n %{libslab}
%{_libdir}/libmate-slab.so.%{slabmaj}*

#---------------------------------------------------------------------------

%package -n %{devslab}
Summary:	Development libraries, include files for MATE control center
Group:		Development/C
Requires:	%{libslab} = %{version}-%{release}

%description -n %{devslab}
This package contains libraries and includes files for developing programs
based on %{name}.

%files -n %{devslab}
%dir %{_includedir}/libmate-slab
%{_includedir}/libmate-slab/*
%{_libdir}/libmate-slab.so
%{_libdir}/pkgconfig/mate-slab.pc

#---------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
#NOCONFIGURE=yes ./autogen.sh
%configure \
	--disable-schemas-compile \
	--disable-update-mimedb \
	%{nil}
%make_build

%install
%make_install

# Fix category field in .desktop files
for desktopfile in %{buildroot}%{_datadir}/applications/*.desktop
do
	desktop-file-edit \
		--remove-category=MATE \
		--add-category=X-MATE \
		$desktopfile
done

# remove unneeded converter
rm -fr %{buildroot}%{_datadir}/MateConf
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

# locales
%find_lang %{name} --with-gnome --all-name
