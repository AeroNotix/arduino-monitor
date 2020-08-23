# Maintainer:  <aaron.l.france@gmail.com>
pkgname=arduino-monitor
pkgver=0.0.1
pkgrel=1
epoch=
pkgdesc="A simple arduino serial-based/i2c hardware monitor"
arch=('i686' 'x86_64')
url=""
license=('GPL')
depends=('python-pyserial')
provides=('arduino-monitor.py')
changelog=
source=(
  arduino-monitor.service
  arduino-monitor.py
)
md5sums=('c5273221ed85346fdc196057aa413441'
         '065bc08a88def7fa0d252e0462c09833')
noextract=()

package() {
  install -Dm644 arduino-monitor.service "$pkgdir/usr/lib/systemd/system/arduino-monitor.service"
  install -Dm644 arduino-monitor.py "$pkgdir/usr/local/bin/arduino-monitor.py"
}

# vim:set ts=2 sw=2 et:
