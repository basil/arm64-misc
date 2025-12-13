#!/usr/bin/env bash
version=4.10.1

tar -xzf $version.tar.gz
cd Rocket.Chat.Electron-$version/
yarn install --immutable --mode=skip-build
tar -czf Rocket.Chat.Electron-$version-yarn-cache.tar.xz .yarn/
mv Rocket.Chat.Electron-$version-yarn-cache.tar.xz ../Rocket.Chat.Electron-$version-yarn-cache.tar.xz
