@echo off
chcp 65001 >nul
echo ========================================
echo  一键上传到 GitHub 构建 APK
echo ========================================
echo.

:: 设置你的 GitHub 用户名
set /p GITHUB_USER="GitHub 用户名: "
set /p REPO_NAME="新建仓库名 (默认 waterpurifier): "
if "%REPO_NAME%"=="" set REPO_NAME=waterpurifier

echo.
echo 请先登录 GitHub:
echo   https://github.com/new
echo   仓库名: %REPO_NAME%
echo   设: Public
echo   不要勾选任何初始化选项
echo.
pause

:: 初始化 git
git init "%REPO_NAME%"
xcopy /E /I /Y waterpurifier_app\* "%REPO_NAME%\"
cd "%REPO_NAME%"

git add -A
git commit -m "小米净水器控制 App"
git branch -M main
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo 按回车后需要输入 GitHub 密码（用 token）:
echo   token 获取: GitHub Settings → Developer settings → Personal access tokens
echo.
pause

git push -u origin main

echo.
echo ========================================
echo  上传完成！
echo  去 GitHub 仓库 Actions 标签查看构建进度
echo  构建完成后下载 bin/waterpurifier-*.apk
echo ========================================
pause
