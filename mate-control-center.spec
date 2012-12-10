%define	major	1
%define	libname	%mklibname mate-window-settings %{major}
%define devname %mklibname -d mate-window-settings

Summary:	MATE control center
Name:		mate-control-center
Version:	1.4.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/%{lua: print (string.match(rpm.expand("%{version}"),"%d+.%d+"))}/%{name}-%{version}.tar.xz

BuildRequires:	docbook-dtd412-xml
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	mate-conf
BuildRequires:	shared-mime-info
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(libebook-1.2)
BuildRequires:	pkgconfig(libmarco-private)
BuildRequires:	pkgconfig(libmate-menu)
BuildRequires:	pkgconfig(libmatekbdui)
BuildRequires:	pkgconfig(libmatenotify)
BuildRequires:	pkgconfig(mateconf-2.0)
BuildRequires:	pkgconfig(mate-desktop-2.0)
BuildRequires:	pkgconfig(mate-doc-utils)
BuildRequires:	pkgconfig(mate-settings-daemon)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	desktop-file-utils

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
Requires:	%{libname} = %{version}

%description -n %{devname}
Development libraries, include files for MATE Control Center

%prep
%setup -q
%apply_patches

%build
NOCONFIGURE=yes ./autogen.sh
%configure2_5x \
	--disable-static \
	--disable-scrollkeeper \
	--disable-update-mimedb

%make LIBS='-lm -lgmodule-2.0'

%install
%makeinstall_std

for desktopfile in %{buildroot}%{_datadir}/applications/*.desktop
do
  desktop-file-edit --remove-category=MATE --add-category=X-MATE $desktopfile
done

find %{buildroot} -name '*.la' -exec rm -f {} \;
rm -f %{buildroot}%{_datadir}/applications/mimeinfo.cache

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc AUTHORS NEWS README
%{_sysconfdir}/mateconf/schemas/control-center.schemas
%{_sysconfdir}/mateconf/schemas/fontilus.schemas
%{_sysconfdir}/mateconf/schemas/mate-control-center.schemas
%{_sysconfdir}/xdg/autostart/mate-at-session.desktop
%{_sysconfdir}/xdg/menus/matecc.menu
%{_bindir}/mate-*
%{_sbindir}/mate-*
%{_libdir}/window-manager-settings/libmarco.so
%{_datadir}/applications/*
%{_datadir}/desktop-directories/matecc.directory
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/mate-control-center
%{_datadir}/mate/cursor-fonts/*
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/polkit-1/actions/org.mate.randr.policy

%files -n %{libname}
%{_libdir}/libmate-window-settings.so.%{major}*

%files -n %{devname}
%{_libdir}/libmate-window-settings.so
%{_libdir}/pkgconfig/*
%{_datadir}/pkgconfig/*
%dir %{_includedir}/mate-window-settings-2.0
%{_includedir}/mate-window-settings-2.0/*