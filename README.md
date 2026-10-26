# ImmortalWrt-Exclusive

ImmortalWrt 稳定版自动定制编译仓库（x86/64 EFI）。

跟踪 ImmortalWrt **正式发布版**（自动跳过 rc/快照，含跨系列），出现新版本自动编译并发布固件到 Releases（tag `ImmortalWrt-<版本>`）。

## 包含组件
| 组件 | 来源 |
|---|---|
| 底座 | [immortalwrt/immortalwrt](https://github.com/immortalwrt/immortalwrt) |
| mihomo 面板 | [nikkinikki-org/OpenWrt-nikki](https://github.com/nikkinikki-org/OpenWrt-nikki) |
| mosdns | [sbwml/luci-app-mosdns](https://github.com/sbwml/luci-app-mosdns) |
| PassWall | [Openwrt-Passwall](https://github.com/Openwrt-Passwall/openwrt-passwall) |
| Argon 主题 | [jerrykuku/luci-theme-argon](https://github.com/jerrykuku/luci-theme-argon) |

固件默认启用 Argon 主题，内置 nikki / PassWall 的 apk 软件源与签名公钥，插件可在 LuCI 软件页在线更新。

## 触发方式
- 定时：每天自动检查上游新版本，有则编译发布，无则跳过
- 手动：Actions → Build ImmortalWrt → Run workflow（可指定版本 / force 强制重编）

## 使用
刷入后出厂参数（旁路由固件）：
- 管理地址：`http://192.168.1.2`（LAN 静态 192.168.1.2/24，网关 192.168.1.1）
- 出厂 DNS：223.5.5.5 / 119.29.29.29（刷完即有网，无需配置）
- 登录：用户名 `root`，密码 `password`

下载 Releases 中的 `generic-ext4-combined*.img.gz`（每次构建同时产出两种启动方式）：
- 传统 BIOS 启动：选 `generic-ext4-combined.img.gz`
- UEFI 启动：选 `generic-ext4-combined-efi.img.gz`
- 已装 OpenWrt 的设备：LuCI → 系统 → 升级固件（按需选择是否保留配置）
- 新设备：dd 写入目标磁盘后启动

定制细节见 `config/`、`files/`、`scripts/` 目录。

## 说明
本仓库与固件不含任何私密信息，构建参数全部在仓库内公开、可复现。
