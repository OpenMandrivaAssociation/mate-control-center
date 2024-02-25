%define mate_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	MATE control center
Name:		mate-control-center
Version:	1.28.0
Release:	1
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		https://mate-desktop.org
Source0:	https://pub.mate-desktop.org/releases/%{mate_ver}/%{name}-%{version}.tar.xz

BuildRequires:	autoconf-archive
BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	mate-common
BuildRequires:	shared-mime-info
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(accountsservice)
BuildRequires:	pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:	pkgconfig(libcanberra-gtk3)
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
BuildRequires:	pkgconfig(udisks2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	pkgconfig(polkit-gobject-1)
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
%license COPYING
%doc AUTHORS NEWS README
%{_sysconfdir}/xdg/menus/matecc.menu
%{_bindir}/mate-*
%{_libdir}/pkgconfig/mate-default-applications.pc
%{_libdir}/pkgconfig/mate-keybindings.pc
%{_datadir}/applications/mate*.desktop
%{_datadir}/desktop-directories/matecc.directory
%{_datadir}/glib-2.0/schemas/org.mate.control-center.gschema.xml
%{_datadir}/glib-2.0/schemas/org.mate.control-center.keybinding.gschema.xml
%{_datadir}/mate-control-center
%{_datadir}/mate-time-admin/
%{_datadir}/mime/packages/mate-theme-package.xml
%{_datadir}/polkit-1/actions/org.mate.randr.policy
%{_datadir}/thumbnailers/mate-font-viewer.thumbnailer
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/hicolor/*/categories/instant-messaging.png
%{_mandir}/man1/mate-*.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
#NOCONFIGURE=yes ./autogen.sh
%configure \
	--disable-schemas-compile \
	--disable-update-mimedb

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

