#!/usr/bin/env bash
version=4.9.2

tar -xzf Rocket.Chat.Electron-$version.tar.gz
cd Rocket.Chat.Electron-$version/
yarn install --immutable --mode=skip-build
tar -czf Rocket.Chat.Electron-$version-yarn-cache.tar.xz .yarn/
mv Rocket.Chat.Electron-$version-yarn-cache.tar.xz ../Rocket.Chat.Electron-$version-yarn-cache.tar.xz
