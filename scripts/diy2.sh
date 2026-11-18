#!/usr/bin/env bash
# diy2: .config 后处理 —— 自动挑选该分支可用的最新内核系列
set -e

echo "== 内核可选系列 =="
grep -oE "config KERNEL_6_[0-9]+" target/linux/Config.in | sort || echo "(该分支不提供内核系列选择，用分支默认)"

NEWEST=$(grep -oE "config KERNEL_6_[0-9]+" target/linux/Config.in | grep -oE "6_[0-9]+" | sort -t_ -k2 -n | tail -1)
if [ -n "$NEWEST" ]; then
  # 只保留最新系列的 y 标记，删掉其它 KERNEL_6_*
  sed -i "/^CONFIG_KERNEL_6_/d" .config
  echo "CONFIG_KERNEL_${NEWEST}=y" >> .config
  echo "== 选定内核系列: 6.${NEWEST#6_} =="
fi

# 保底：确保关键包没被依赖求解丢掉
for k in CONFIG_TARGET_ROOTFS_PARTSIZE=976 \
         CONFIG_PACKAGE_luci-app-nikki=y \
         CONFIG_PACKAGE_mihomo-meta=y \
         CONFIG_PACKAGE_luci-app-mosdns=y \
         CONFIG_PACKAGE_luci-app-passwall=y \
         CONFIG_PACKAGE_luci-theme-argon=y \
         CONFIG_PACKAGE_luci-app-upnp=y; do
  key=${k%%=*}
  grep -q "^${key}=y$" .config || grep -q "^${key}=976$" .config || echo "$k" >> .config
done

# 关掉 apk 时代的默认瘦身/无关大件（若存在）
sed -i 's/^CONFIG_PACKAGE_luci-app-turboacc=y/# &/' .config || true

echo "diy2 done"
