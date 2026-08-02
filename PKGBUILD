pkgname=downloadtracks
pkgver=1.0.0
pkgrel=1 
pkgdesc="CLI/GUI py program for audio download from youtube"
arch=('any')
url="https://github.com/Progress-ux/DownloadTracks"
license=('MIT')

depends=(
  'python' 
  'ffmpeg' 
  'yt-dlp' 
  'python-mutagen'
  'python-requests'
)

source=(
  'main_cli.py'
  'LICENSE'
  'README.md'
)
sha256sums=(
  'SKIP'
  'SKIP'
  'SKIP'
)

package() {
  cd "$startdir"

  install -d "$pkgdir/usr/lib/$pkgname"
  install -d "$pkgdir/usr/bin"

  cp -r --preserve=mode,ownership \
      core infrastructure \
      main_cli.py LICENSE README.md \
      "$pkgdir/usr/lib/$pkgname"

  chmod +x "$pkgdir/usr/lib/$pkgname/main_cli.py"

  ln -s "/usr/lib/$pkgname/main_cli.py" "$pkgdir/usr/bin/$pkgname"
}
