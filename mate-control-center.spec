%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	major	1
%define	libname	%mklibname mate-window-settings %{major}
%define devname %mklibname -d mate-window-settings

%define	slabmaj	0
%define	libslab	%mklibname mate-slab %{slabmaj}
%define	devslab	%mklibname -d mate-slab

Summary:	MATE control center
Name:		mate-control-center
Version:	1.14.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	shared-mime-info
BuildRequires:	yelp-tools
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(libebook-1.2)
BuildRequires:	pkgconfig(libmarco-private)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(libmatekbdui)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(mate-settings-daemon)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(unique-3.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xxf86misc)

Requires:	mate-settings-daemon
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	shared-mime-info

%description
MATE Control-center is a configuration tool for easily
setting up your MATE environment.

%package -n %{libname}
Summary:	Shared library for MATE control center
Group:		System/Libraries

%description -n %{libname}
This package contains the shared library for MATE Control Center

%package -n %{devname}
Summary:	Development libraries, include files for MATE control center
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development libraries, include files for MATE Control Center

%package -n %{libslab}
Summary:	Shared library for MATE control center
Group:		System/Libraries

%description -n %{libslab}
This package contains the shared library for MATE Control Center

%package -n %{devslab}
Summary:	Development libraries, include files for MATE control center
Group:		Development/C
Requires:	%{libslab} = %{version}-%{release}

%description -n %{devslab}
Development libraries, include files for MATE Control Center

%prep
%setup -q
%apply_patches
NOCONFIGURE=yes ./autogen.sh

%build
%configure \
	--disable-update-mimedb \
	--with-gtk=3.0

%make

%install
%makeinstall_std

for desktopfile in %{buildroot}%{_datadir}/applications/*.desktop
do
	desktop-file-edit --remove-category=MATE --add-category=X-MATE $desktopfile
done

# remove unneeded converter
rm -fr %{buildroot}%{_datadir}/MateConf
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc AUTHORS NEWS README
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
%{_datadir}/mate/cursor-fonts/*
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_mandir}/man1/mate-*.1*

%files -n %{libname}
%{_libdir}/libmate-window-settings.so.%{major}*

%files -n %{devname}
%{_libdir}/libmate-window-settings.so
%{_libdir}/pkgconfig/mate-default-applications.pc
%{_libdir}/pkgconfig/mate-keybindings.pc
%{_libdir}/pkgconfig/mate-window-settings-2.0.pc

%dir %{_includedir}/mate-window-settings-2.0
%{_includedir}/mate-window-settings-2.0/*

%files -n %{libslab}
%{_libdir}/libmate-slab.so.%{slabmaj}*

%files -n %{devslab}
%{_libdir}/libmate-slab.so
%{_libdir}/pkgconfig/mate-slab.pc
%dir %{_includedir}/libmate-slab
%{_includedir}/libmate-slab/*

