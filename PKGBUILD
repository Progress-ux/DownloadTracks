pkgname=DownloadTracks
pkgver=1.0.0
pkgrel=1 
pkgdesc="CLI/GUI py program for audio download from youtube"
arch=('any')
url="https://github.com/Progress-ux/DownloadTracks.git"
license=('MIT')

depends=(
  'python' 
  'ffmpeg' 
  'yt-dlp' 
  'python-mutagen'
  'python-requests'
)

source=("git+https://github.com/Progress-ux/${pkgname}.git")
sha256sums=('SKIP')

package() {
  cd "$srcdir/$pkgname"

  install -d "$pkgdir/usr/lib/$pkgname"
  install -d "$pkgdir/usr/bin"

  cp -a . "$pkgdir/usr/lib/$pkgname/" 

  ln -s "/usr/lib/$pkgname/main_cli.py" "$pkgdir/usr/bin/$pkgname"
  chmod +x "$pkgdir/usr/lib/$pkgname/main_cli.py"
}
