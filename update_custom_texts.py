import os
import json
from bs4 import BeautifulSoup

html_files = ["danang.html", "halong.html", "hoian.html", "ninhbinh.html", "phuquoc.html", "sapa.html"]

custom_data = {
    "Bà Nà Hills - Cầu Vàng Tiên Cảnh": {
        "adv": "🌟 ĐIỂM SĂN MÂY SỐ 1 ĐÀ NẴNG: Dạo bước trên hai bàn tay Phật khổng lồ",
        "desc": "Cầu Vàng tại Sun World Ba Nà Hills không chỉ là một cây cầu, mà là một tác phẩm nghệ thuật đỉnh cao vươn ra thế giới. Cảm giác được dạo bước giữa lưng chừng trời mây xanh thẳm, ngắm nhìn khung cảnh ngoạn mục của núi rừng Bà Nà sẽ là trải nghiệm nhớ đời. Đừng quên mang theo một bộ cánh lộng lẫy để có những thước phim 'cinematic' lung linh không thua kém gì các MV ca nhạc thế giới.",
        "time": "Lịch trình khuyên đi: 07:00 - Sáng Ngày 2 (Tránh cảnh quá đông đúc lúc trưa)"
    },
    "Biển Mỹ Khê cát trắng đẹp hành tinh": {
        "adv": "🏄‍♂️ BÃI BIỂN QUYẾN RŨ NHẤT HÀNH TINH (Bình chọn bởi Forbes)",
        "desc": "Biển Mỹ Khê sở hữu bãi cát trắng mịn, thoai thoải và làn nước xanh ngắt vô cùng lý tưởng để tắm mát và thả lướt ván. Sóng biển Mỹ Khê đặc biệt ôn hòa, phù hợp cho mọi lứa tuổi bơi lội. Bạn có thể nằm dài dưới bóng dừa, nhâm nhi ly cocktail và ngắm hoàng hôn đỏ cam đang dần buông xuống biển cả vô tận.",
        "time": "Lịch trình khuyên đi: 16:30 - Chiều Ngày 1 (Khoảng thời gian lý tưởng ngắm hoàng hôn)"
    },
    "Chinh Phục Thắng Cảnh Ngũ Hành Sơn": {
        "adv": "⛰️ LINH THIÊNG VÀ HUYỀN BÍ: Khám phá chuỗi 5 ngọn núi tuyệt đẹp",
        "desc": "Ngũ Hành Sơn là một quần thể gồm 5 ngọn núi đá vôi nhô lên sừng sững giữa bầu trời Đà Thành. Đây là nơi hội tụ tinh hoa đất trời với rất nhiều hang động tự nhiên (Động Huyền Không, Âm Phủ) và đền chùa cổ kính ngàn năm tuổi. Bạn sẽ phải đi bộ khám phá hệ thống bậc thang đá phong rêu mờ ảo để tận hưởng sự thanh tịnh hiếm có.",
        "time": "Lịch trình khuyên đi: 08:00 - Sáng Ngày 3 (Trời mát mẻ không quá mệt khi leo dốc)"
    },
    "Bán đảo Sơn Trà & Chùa Linh Ứng": {
        "adv": "🗽 TƯỢNG PHẬT BÀ QUAN ÂM CAO NHẤT VIỆT NAM (67m)",
        "desc": "Bán đảo Sơn Trà được ví như 'Lá phổi xanh' của Đà Nẵng, đây cũng là ngôi nhà của loài Voọc Chà Vá chân nâu quý hiếm. Chùa Linh Ứng bãi Bụt linh thiêng tọa lạc trên sườn núi nổi bật với pho tượng Phật Bà Quan Âm có tầm nhìn ôm trọn eo biển Đà Nẵng. Ai muốn câu bình an may mắn thì không đâu tuyệt vời bằng ngôi chùa này.",
        "time": "Lịch trình khuyên đi: 15:30 - Chiều Ngày 2 (Dạo mát và xua tan phiền não rảo bộ bóng râm)"
    },
    "Chợ Cồn - Thiên đường sành ăn": {
        "adv": "🍢 CHỢ ĐỊA PHƯƠNG SẦM UẤT: 100K Ăn sập Đà Nẵng!!",
        "desc": "Khu ẩm thực Chợ Cồn luôn khiến du khách trầm trồ bởi hàng tá những món ăn vặt miền Trung truyền thống. Bánh bèo, nậm, lọc nức rưới nước mắm chua ngọt, kem bơ mát lạnh hay đĩa mít trộn dai dai siêu cay sẽ làm điêu đứng mọi tín đồ ẩm thực. Ẩm thực tại đây minh chứng cho sự tinh tế trong khẩu vị của người dân Đà Nẵng: ngon, bổ, rẻ.",
        "time": "Lịch trình khuyên đi: 15:00 - Chiều Ngày 3 (Thời điểm cực thịnh các quầy chè mạn hoạt động)"
    },
    "Cầu Rồng Phun Lửa sực đỉnh": {
        "adv": "🔥 HUYỀN THOẠI ĐÀ THÀNH: Cảnh tượng rồng vàng nhả lửa về đêm",
        "desc": "Từ lâu Cầu Rồng đã trở thành dấu ấn mạnh mẽ nhất khiến Đà Nẵng khác biệt mọi thành phố. Thiết kế dáng rồng vươn khơi mạnh mẽ, thân cầu uốn lượn được trải vô số đèn Led rực rỡ vàng óng ánh. Hãy đứng dọc hai đầu cầu hoặc ngồi tại bờ sông Hàn uống nước chanh để xem rồng phun lửa ầm ầm và xả bọt nước sảng khoái.",
        "time": "Lịch trình khuyên đi: 20:30 - Tối Thứ 7, Chủ Nhật (Sự kiện phun Lửa & Nước duy nhất)"
    },
    
    # Halong
    "Khu vui chơi Sun World": {
        "adv": "🎢 TỔ HỢP GIẢI TRÍ VƯỢT THỜI GIAN ĐẦU TƯ BỞI SUN GROUP",
        "desc": "Trải dài trên diện tích rộng lớn tại Bãi Cháy, Sun World có hệ thống Cáp treo Nữ Hoàng vượt biển lớn nhất thế giới. Không chỉ thế, Vòng quay Mặt Trời Sun Wheel ngắm toàn cảnh Vịnh, khu Công viên Rồng (Dragon Park) cực kích thích với các đường lượn siêu tốc sẽ giúp bạn xả stress vô cùng bứt phá.",
        "time": "Lịch trình khuyên đi: Cả Ngày 2 (Để tham gia đủ loại từ Công viên nước đến trò mạo hiểm)"
    },
    "Vịnh biển Lan Hạ đẹp nguyên sơ": {
        "adv": "⛵ VIỆN NGỌC LẲNG LẶNG NGỦ QUÊN: Ít xô bồ, nhiều thư thái",
        "desc": "Nối liền kề với Di sản thiên nhiên thế giới Hạ Long, Vịnh Lan Hạ có tới 400 hòn đảo phủ đầy thảm thực vật xanh biếc nguyên thủy. Ở đây thu hút du khách bởi các bãi tắm nước trong vắt phẳng lặng len lỏi giữa núi đá vôi. Bạn có thể thuê thuyền Kayak tự mình luồn lách qua những hàng động tối om rợn ngợp để tận hưởng cảm giác chinh phục tự nhiên.",
        "time": "Lịch trình khuyên đi: 14:00 - Chiều Ngày 3 (Chèo Kayak dưới bóng vách núi, ánh ráng chiều tà)"
    },
    "Bảo tàng Quảng Ninh Đen huyền": {
        "adv": "📸 ĐIỂM CHỤP LOOKBOOK CỰC SANG CHẢNH: Kiến trúc độc bản mỏ than đen",
        "desc": "Tòa nhà với thiết kế mặt kính đen nhánh nổi bật nguyên tấm khối, phản chiếu trọn vẹn hình ảnh vịnh biển phía chân trời rộng thênh thang. Bên trong Bảo Tàng Quảng Ninh lưu giữ rất nhiều kiến thức về quá trình hình thành lớp vỏ sinh học Vịnh và truyền thống cần mẫn tại xứ sở 'Vàng Đen'.",
        "time": "Lịch trình khuyên đi: 09:00 - Sáng Ngày 4 (Điểm tham quan nhẹ nhàng trong nhà)"
    },
    "Đảo ngọc Tuần Châu xa hoa": {
        "adv": "🛳️ CẢNG TÀU SẦM UẤT VÀ KHU NGHỈ DƯỠNG CẬP BẾN GIỚI SIÊU GIÀU",
        "desc": "Cảng du thuyền Tuần Châu là cửa ngõ lớn nhất dắt bạn ra tới lòng vịnh kỳ vĩ. Trên đảo có bãi biển nhân tạo thoai thoải dài ngút tầm mắt và khu show diễn hải cẩu, sư tử biển hay nhạc nước rất vui nhộn phù hợp gia đình có trẻ em.",
        "time": "Lịch trình khuyên đi: 08:30 - Sáng Ngày 1 (Trung chuyển ra thuyền lớn ngủ đêm trên vịnh)"
    },
    "Phố ẩm thực Chợ đêm Bãi Cháy": {
        "adv": "🦐 HẢI SẢN TƯƠI SỐNG LƯỚI VỀ TRONG NGÀY DẬP DÌU THƠM NGON",
        "desc": "Trải dài hàng trăm gian hàng sát bên bờ biển Hạ Long sầm uất, Chợ đêm có đủ thứ: Đồ lưu niệm thủ công mỹ nghệ, Ngọc Trai lấp lánh và nhất định phải kể đến đồ Hải sản nướng tươi sống - Mực nháy, ngán, tu hài, cua Cà Mau. Tiếng xèo xèo của than hoa hòa lẫn với làn gió biển thổi tung bay mệt mỏi.",
        "time": "Lịch trình khuyên đi: 19:30 - Tối Ngày 1 & 2 (Ăn uống nhậu nhẹt hải sản say sưa)"
    },
    "Đảo Cát Bà hoang dã": {
        "adv": "🌿 KHU DỰ TRỮ SINH QUYỂN THẾ GIỚI - Xanh ngút ngàn và rậm rạp",
        "desc": "Đảo Cát Bà có một khu vườn quốc gia rậm rạp được UNESCO coi trọng tuyệt đối. Hệ sinh thái này là hệ sinh thái hỗn hợp kết hợp rừng thường xanh nhiệt đới rậm rạp và biển đa dạng chủng loại hải dương. Thuê một chiếc xe tay ga chạy vòng quanh Cát Bà ngắm trọn biển và đường rừng là kỷ niệm dân phượt rất thích.",
        "time": "Lịch trình khuyên đi: Cả Ngày 3 (Trekking Rừng Quốc gia Cát Bà hoặc Tắm bãi Cát Cò)"
    },

    # Hoian
    "Cù Lao Chàm, Đảo Ngọc Cù Lao": {
        "adv": "🤿 THIÊN ĐƯỜNG LẶN NGẮM SAN HÔ BẬC NHẤT DI SẢN MÙA HÈ",
        "desc": "Trải nghiệm dập dềnh ngồi cano cao tốc cực đã lao phăng phăng xé tan đợt sóng biển. Cù Lao Chàm lưu giữ những điều nguyên sơ nhất với hệ san hô tuyệt diện dưới làn nước tinh khiết trong vắt thấu đáy rạng màu huỳnh quang hoang sơ.",
        "time": "Lịch trình khuyên đi: 08:00 - Sáng Ngày 2 (Dành nguyên nửa ngày lặn sóng tắm mát)"
    },
    "Rừng Dừa Bảy Mẫu Cẩm Thanh": {
        "adv": "🥥 MIỀN TÂY THU NHỎ TRONG LÒNG HỘI AN: Trải nghiệm múa Thúng có một không hai",
        "desc": "Ngồi len lỏi trên chiếc thuyền thúng tròn vành vạnh truyền thống chui vào từng kẽ khe rạch chằng chịt rợp bóng dừa xanh mát của Cẩm Thanh sẽ xua tan đi cái oi ả gay gắt. Các nghệ nhân chèo thuyền sẽ có một màn trình diễn quay thúng lốc xoáy lộn tùng phèo cực vui nhộn cùng âm nhạc EDM sôi động.",
        "time": "Lịch trình khuyên đi: 15:30 - Chiều Ngày 2 (Ánh chiều tà chụp ảnh rặng dừa màu vàng nhạt tuyệt đẹp)"
    },
    "Di sản Thánh địa Mỹ Sơn": {
        "adv": "🗺️ VƯƠNG QUỐC CHĂM PA XƯA: Kỳ bí di sản gạch nung sụp đổ rêu phong",
        "desc": "Cách Hội An gần một tiếng đồng hồ chạy ô tô, thánh địa Mỹ Sơn có tuổi đời từ hàng nghìn thế kỷ tồn tại âm thầm giữa thung lũng dốc sâu thẳm. Đi dạo giữa các ngọn tháp mòn đất thiêng để thưởng thức điệu múa bóng của các thiếu nữ Chàm uyển chuyển hoài niệm quá khứ vĩ đại.",
        "time": "Lịch trình khuyên đi: 07:30 - Sáng Ngày 3 (Tránh ánh nắng trưa cực nóng ở thung lũng)"
    },
    "Bãi biển An Bàng thơ mộng": {
        "adv": "🍹 BÃI BIỂN CHILL NHẤT CHÂU Á KHÔNG ỒN ÀO VÀ ĐẦY TRƠN VẮNG XÔ BỒ",
        "desc": "An Bàng không như những bãi biển sầm uất chen chúc khác. Người ta tới An Bàng để tìm sự 'Tĩnh Cổ' văng vẳng nghe tiếng bọt xô vào bờ cát mịn màng. Cắm một chiếc ô vòm lá dừa dạo một cốc bia hơi, mở bản nhạc nhẹ và chiêm ngưỡng đám trẻ con thả diều trên bờ thoai thoải.",
        "time": "Lịch trình khuyên đi: 16:30 - Chiều Ngày 1 (Thời gian vàng thả lỏng sau khi hạ cánh, Check-in khách sạn)"
    },
    "Làng Lụa Hội An cổ truyền": {
        "adv": "👘 BỨC TRANH LỤA TƠ TẰM NGHÌN NĂM CÓ TỪ THẾ KỶ 17",
        "desc": "Bạn sẽ trực tiếp trải nghiệm thu hoạch dâu non, cho tằm ăn, và ngồi gỡ kén se sợi trên bàn cửi gỗ cũ mèm kêu kẽo kẹt tiếng thời gian do các vị bô lão trực tiếp dệt. Mua sắm lụa tơ tằm thật nguyên chất óng ánh sẽ là món lưu niệm cực kỳ đáng giá ở đây.",
        "time": "Lịch trình khuyên đi: 09:30 - Sáng Ngày 4 (Hoạt động nhàn nhã thích hợp mua sắm trước khi về)"
    },
    "Làng Gốm Thanh Hà nghìn năm": {
        "adv": "🏺 VỌT NẶN ĐẤT SÉT CÙNG CÁC NGHỆ NHÂN LÃO LÀNG ĐẠI TÀI",
        "desc": "Thanh Hà làm gốm bằng tay tỉ mẩn miệt mài không máy móc. Từng phôi đất đỏ gạch dọc lưu hành con sông Thu Bồn được vuốt cẩn trọng từng góc cạnh. Bạn hãy ghé Công viên đất nung Terra Cotta để check-in cùng tượng danh lam thế giới đúc gốm 100% rực rỡ dưới ánh nắng miền Trung rát.",
        "time": "Lịch trình khuyên đi: 14:00 - Chiều Ngày 3 (Tự tay làm gốm và mua tò he ngộ nghĩnh)"
    },
    
    # Ninhbinh
    "Chùa khổng lồ Bái Đính tự": {
        "adv": "🛕 QUẦN THỂ CHÙA NẮM KỶ LỤC CHÂU Á - Rộng 539ha và Đồ sộ ngộp thở",
        "desc": "Chùa Bái Đính bao phủ cả một vùng núi đá mênh mông, sở hữu bức tượng Phật dát vàng nặng tới 100 tấn và hàng nghìn bức La Hán tạc bằng đá nguyên khối chạy dọc quanh hành lang dài dằng dặc. Đêm xuống hệ thống đèn thắp lên nơi này tựa vương đô sáng chói huyền bí.",
        "time": "Lịch trình khuyên đi: 07:30 - Sáng Ngày 2 (Dạo quanh thưa vắng người đi lễ viếng không ồn)"
    },
    "KDL Chim Sinh Thái Thung Nham": {
        "adv": "🦩 THUNG LŨNG NGẬP NƯỚC - Vương chim cò bay rợp trời vào mỗi buổi hoàng hôn",
        "desc": "Thư thả ngồi mạn xuồng gỗ mộc trôi chậm dọc theo con lạch ngập nước, bạn sẽ được thưởng ngoạn cảnh sắc thiên nhiên hiếm thấy trên đời khi hàng vạn vạn cánh chim trời (cò, vạc, hằng hạc) chao rợp bóng bay lượn che kín rặng tre già đổ về tìm tổ đẻ.",
        "time": "Lịch trình khuyên đi: 16:30 - Chiều Ngày 2 (Thời khắc duy nhất trong ngày hàng vạn chim chao liệng bay về tổ)"
    },
    "Khu Bảo Tồn Nước Vân Long": {
        "adv": "🪷 'VỊNH KHÔNG SÓNG' ĐÓNG PHIM BONGBUSTERS HOLLYWOOD 'KONG: SKULL ISLAND'",
        "desc": "Toàn cảnh Đầm Vân Long phẳng lặng y như tấm kính tấm khổng lồ soi rạn bầu trời và dãy núi non Tràng An hùng vĩ. Thỉnh thoảng một chiếc xuồng nan nhỏ cắm cây sào rẽ luồng cỏ lác rậm rạp lướt qua để lại đường gợn nước thanh khiết. Phải đến Vân Long bạn mới hiểu cái đẹp bình dị nhất đôi khi làm lòng yên bình vô cùng.",
        "time": "Lịch trình khuyên đi: 08:00 - Sáng Ngày 3 (Sương khói bốc lên mặt nước lãng đãng đẹp tuyệt trần)"
    },
    "Vạn Lý Trường Thành Hang Múa": {
        "adv": "🏔️ CUNG ĐƯỜNG ĐIỂM SĂN ẢNH ĐẸP NHẤT NINH BÌNH TRÊN CAO",
        "desc": "Với 486 bậc thang đá khắc chạm hình trạm trổ dẫn vút cao lên ngọn núi Múa gồ ghề dốc đứng, đây quả thực là 'Vạn Lý Trường Thành' của duy nhất Ninh Bình. Vượt qua đoạn dốc nhọc nhằn, lên đỉnh với hình rồng chầu mặt ngọc bạn sẽ thâu tóm được cả thung lũng Tam Cốc - những mảng vá lúa mùa chín rực rỡ ngập nước như tranh sơn dầu.",
        "time": "Lịch trình khuyên đi: 15:30 - Chiều Ngày 1 (Lúc ráng chiều nắng chiếu ngang ngọn lúa Tam Cốc chín vàng)"
    },
    "Tuyệt tình cốc Âm Ti (Động Am Tiên)": {
        "adv": "🐲 TUYỆT TÌNH CỐC RỜI XA TRẦN THẾ VÀ TÁCH BIỆT THẾ GIAN TRONG TIỂU THUYẾT",
        "desc": "Phải đi qua chặng hầm chui dài tăm tối và vách núi khép để ló ra một Động Am Tiên tĩnh mịch. Nơi đây gắn liền với truyền thuyết thời nhà Đinh với mặt hồ hình móng ngựa bốn bề đều là rặng núi cấm sâu thẳm hiểm trở vút lồng lên trời ngỡ tựa chốn thâm cốc hiểm nghìn năm.",
        "time": "Lịch trình khuyên đi: 10:00 - Sáng Ngày 2 (Nắng lên xuyên thủng làn mây lờn vờn hồ Ao Giải)"
    },
    "Di tích Cố đô cổ xưa Hoa Lư": {
        "adv": "👑 TRẦN TRONG ÂM HƯỞNG LỊCH SỬ KINH ĐÔ VỮNG CHÃI THỜI ĐINH-LÊ",
        "desc": "Một vương triều vàng son của dân tộc gói gọn trong khu di tích Cố Đô Hoa Lư với tường thành là trùng trùng điệp điệp núi non tự nhiên làm khiên chắn vững mạnh. Đứng lặng đi để thắp nén hương trên ngai của vua Đinh Tiên Hoàng Đế và lắng tai nghe vị hướng dẫn viên kể câu chuyện cờ lau tập trận rưng rưng máu lửa tự hào dân tộc oanh liệt.",
        "time": "Lịch trình khuyên đi: 09:00 - Sáng Ngày 1 (Điểm đỗ ngay sớm để thấu hiểu trước bề dày lịch sử ngàn năm)"
    },
    
    # Phuquoc
    "Thị trấn Hoàng Hôn Sunset Town": {
        "adv": "🌅 THỊ TRẤN ĐỊA TRUNG HẢI KỀ CẬN LƯỜI BIẾNG BÊN BỜ NAM ĐẢO",
        "desc": "Với kiến trúc mảng tường tróc phôi vữa được tính toán giả cổ nghệ thuật tạo sự nồng đậm chất men phong cách thị trấn Amalfi nước Ý xa xôi, thị trấn Sunset Town là một điểm có khả năng hớp hồn du khách. Phải tới đây uống ly nước cam ngắm nhìn Tháp Đồng Hồ trung tâm lừng lững ngay trên nền vịnh Thái Lan thẳm xanh mướt mát hiếm hoi.",
        "time": "Lịch trình khuyên đi: 17:00 - Chiều Ngày 2 (Tên trịnh trọng phải thưởng thức đúng thời khắc buông rũ Hoàng hôn tím xám cực nét)"
    },
    "Thành phố Venice trong lòng Grand World": {
        "adv": "🛶 THÀNH PHỐ KHÔNG NGỦ THỨC TRỌN 24/7 DÀNH PHÚ VĂN CHƠI",
        "desc": "Nhạc EDM DJ, hội diễn show tinh hoa, đi thuyền độc mộc Gondola xuôi lững lờ theo dòng kênh len lỏi lấp loáng kiến trúc Châu Âu... Mọi thứ tại Phú Quốc United Center - Grand World đều lộng lẫy và rực pháo vỡ trời không màng ngủ nghỉ cho giới tiệc tùng xả stress vô giới hạn căng đét ngợp thở choáng ngợp tráng lệ.",
        "time": "Lịch trình khuyên đi: 19:30 - Tối Ngày 1 & Ngày 2 (Vui nhộn náo nhiệt show âm nhạc EDM và Lazer ánh sáng)"
    },
    "Nhà tù Côn Đảo Phú Quốc": {
        "adv": "⛓️ KHÚC TRÁNG CA LAO TÙ PHÚ QUỐC XÉ LÒNG TRỜI NAM",
        "desc": "Khác lạ với sự lộng lẫy hào nhoáng thường thấy của Đảo Ngọc, chốn lao tù lịch sử Phú Quốc đem lại sự xúc động với sự thật chân thực qua hàng ngàn tượng sáp về những màn tra khảo rùng rợn đến nghẹn máu. Bất cứ người Việt Nam nào khi đặt lẵng hoa tưởng niệm tại đài liệt sỹ sẽ thấm thía hòa bình ngày nay phải đổi trả bằng điều gì bi tráng oanh liệt nhất.",
        "time": "Lịch trình khuyên đi: 08:30 - Sáng Ngày 4 (Một nốt gợn trầm lắng đọng đầy sâu thẳm trước khi chia tay đảo ngọc)"
    },
    "Vút Xích đu tiên tại Bãi Sao mát lạnh": {
        "adv": "🏖️ CHECK-IN VỚI CÂY DỪA ĐỔ 'HUYỀN THOẠI' BỀ BỀ TÁP NƯỚC",
        "desc": "Bãi Sao không hổ danh là bãi tắm có làn cát mịn nhuyễn tơ mềm mại tinh khiết bậc nhất tại Việt Nam. Không những vậy vùng biển lặn cạn thoải kéo dài rất lý tưởng vấp ngã vùng vẫy bơi và rực rỡ với hàng nghìn chú sao biển. Lắc lư qua lăng kính Xích đu tiên trên cây dừa lá xoè hướng ra biển cả đem lại thước phim quay chậm cực sảng khoái mát lành.",
        "time": "Lịch trình khuyên đi: Cả Sáng Ngày 2 (Dành nguyên để tắm nắng lăn lộn với sóng biển không cồn)"
    },
    "Băng vịnh bằng Cáp Treo Hòn Thơm": {
        "adv": "🚡 CÁP TREO VƯỢT BIỂN DÀI NHẤT THẾ GIỚI MANG KỶ LỤC GUINNESS",
        "desc": "Vắt ngang qua ngút ngàn mênh mông vũng neo đậu tàu bè của các cụp đảo Hòn Dừa rực rõ đầy chằng chịt thuyền ghe làm xiếc thăng bằng khép khíp như mê cung nước thẳm. Đi cáp treo lơ lửng sương chiều này mang sự kỳ diệu mạo hiểm, mở ra công viên nước thuỷ cung nhộn nhịp huyên náo cho cả gia đình phá lưới tại Hòn Thơm xa tận tít mù.",
        "time": "Lịch trình khuyên đi: 09:30 - Sáng Ngày 3 (Bắt đầu một ngày trải nghiệm chơi xả ga tại Aquatopia)"
    },
    "Tuyệt tác nghệ thuật Kiss Bridge": {
        "adv": "💋 BIỂU TƯỢNG TÌNH YÊU CHẠM NHAU ĐỨT QUÃNG GIỮA TRỜI VÀ MẶT KHƠI",
        "desc": "Hai mảng uốn cong khổng lồ vươn mình đứt gãy mà chẳng hề kết dính chỉ cách một đốt ngón tay ở khoảng giữa chân không với bầu trời. Ở Kiss Bridge (Cầu Hôn), khoảnh khắc mặt trời rực lịm trần thả lồng vào kẽ hở chia đôi ánh ngọc là một điểm nhấn cực đỉnh cao kiến trúc siêu tinh tế mà vị kỹ sư Marco Casamonti đem gieo rắc lãng mạn vô bến cho cặp tình nhân.",
        "time": "Lịch trình khuyên đi: 17:15 - Chiều Ngày 3 (Săn hoàng hôn lồng bóng tình yêu duy nhất)"
    },

    # Sapa
    "Chinh phục Đèo Ô Quy Hồ": {
        "adv": "🏍️ LƯỢN CUNG ĐƯỜNG ĐÈO 'TỨ ĐẠI ĐỈNH ĐÈO' LÚC TRỜI ĐỔ MÂY RỢP",
        "desc": "Đèo Ô Quy Hồ vươn mình bao quanh những mép vực sâu hoắm hút lửng đứt hơi tạo cảm giác nghẹt thở mạnh mẽ sảng khoái thách thức thần kinh. Ở độ cao gần hai nghìn mét tót ngút lên trời, ngồi tại chòi mây uống chén chà tuyết và xem mây mù rẽ dọc con đường vọt lộn là trải nghiệm 'Sapa rực lửa' cho hội cuồng phượt phiêu du lãng tử miền núi.",
        "time": "Lịch trình khuyên đi: 15:00 - Chiều Ngày 2 (Ánh nắng xẻ núi xiên xuống những thung lũng lượn khói sương)"
    },
    "Làng sống Mây Bản Tả Van": {
        "adv": "🌾 NƠI NÀY 'LẶNG THẾ', ẨN MÌNH SÂU THẲM CHỈ CÓ LÚA VÀ TIẾNG KÈN DAO",
        "desc": "Để mặc thị trấn Sapa náo nhiệt bê tông, Tả Van dẫn ta vòng vèo tít tắp sâu dọc theo dốc vách xuống thung lũng Mường Hoa nơi dân bản trải dải ruộng bậc thang tầng lớp nếp đan khin chít cuồn cuộn sức sống lác đác những vách lá gỗ nhuộm đen muội bếp than của người Hmông đỏ sột soạt sương rơi lạnh cóng tĩnh tâm xả street bộn bề áp lực gánh vác trần gian.",
        "time": "Lịch trình khuyên đi: Cả Sáng Ngày 3 (Đi bộ Trekking lấm bùn len lỏi đâm rễ vào những khóm bản xa tẻo xa teo)"
    },
    "Mùa Đào ngắt Đồi chè Ô Long": {
        "adv": "🌸 RỪNG MAI ANH ĐÀO VÀNG RỘ KHOE SẮC RỰC LỬA CUỐN MÊ TÂM",
        "desc": "Chẳng cần tới Nhật Bản phù hoa, bạn chỉ cần canh đi đồi chè Ô Long. Những cây mai anh đào lá hồng được vun mọc thẳng hàng che dọc dăm lối hàng chè xanh ngắt non tạo bức tranh hòa cọ thiên nhiên tuyệt đẹp khó xé bức rạch nét chê để tung váy lưu trọn thước phim kỷ niệm tinh sương đọng nước hạt li ti dính áo mùa xuân miền núi hùng vì.",
        "time": "Lịch trình khuyên đi: 07:30 - Sáng Ngày 1 (Ban mai tia nắng xuyên kẽ lốc lá mai anh đào sương đọng cực nghệ)"
    },
    "Chiêu bái Bản Cát Cát": {
        "adv": "🎎 HÓA THÂN 'CÔ GÁI BẢN' TẠI NGÔI LÀNG CỔ NHẤT VÀ ĐẸP BẬC TƯ",
        "desc": "Cát Cát rầm rập những cọn nước guồng gỗ kĩu kịt rên rỉ rêu phong phả làn hơi bọt trắng xóa bốc sương khi thác Tiên tung trào gầm rú. Bỏ vài trăm ngàn để khoác lên bộ đồ sặc sỡ đính chỉ cườm chít rực thổ cẩm rảo bước leng keng bạc nén lên từng bậc đá sỏi tạo thước phim cực ngầu chẳng chê ném đi đâu khoảnh khắc sống núi vô vàn sắc điệu ngập sắc.",
        "time": "Lịch trình khuyên đi: 08:30 - Sáng Ngày 2 (Mặc áo dân tộc lang thang chợ phiên mua táo mèo chua ngọt)"
    },
    "Kiến trúc tháp Sun Plaza": {
        "adv": "🏰 TÒA NHÀ GA TÀU HỎA HOA LỆ TỰA LÂU ĐÀI CHÂU ÂU CHÍNH HIỆU",
        "desc": "Nổi chễm chệ tráng lệ tông vàng hổ phách và xám đá ở ngay vòng xoay ngã tư duy nhất trung tâm Sapa. Bức tường đồng hồ tháp khổng lồ rêu phong Pháp cổ kính khắc phác tỉ mỉ đường nét sang chảnh cho phép rảo bước chụp check-in cực lạnh lùng Tây phương sang chảnh dắt tay nhau dạo bến tàu leo đỉnh mây lác đác rình rang.",
        "time": "Lịch trình khuyên đi: 20:00 - Tối Ngày 1 (Đèn lồng vàng soi rọi toàn tháp tráng lệ ngả bóng trung tâm phồn thực)"
    },
    "Tượng Phật trên đỉnh Fansipan": {
        "adv": "☁️ NÓC NHÀ ĐÔNG DƯƠNG RỘNG LỚN ÔM GÓI THẦN LINH BẦU TRỜI NGUYÊN BẢN",
        "desc": "Chạm ngón tay băng đá tới mỏm đỉnh Fansipan - ở độ cao 3.143 mét mây bay lổn nhổn sát mặt mũi thở sùi bọt tuyết. Ngắm Đại Phật rực sừng sững dốc vực lửng lơ trên biển mây bông quánh mù đặc nhấp nhô lốc thốc núi xanh vờn, thắp một nén nhang ngửi không khí đông cứng khói sương dập dờn sẽ thấu trọn cõi niết bàn lác mắt.",
        "time": "Lịch trình khuyên đi: 09:00 - Sáng Ngày 2 (Dành nửa ngày để chinh phục núi vĩ đại và nhâm nhi cafe mây cõi thiên)"
    }
}

for filename in html_files:
    filepath = os.path.join("d:\\Websitedulich", filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".suggested-card")
    for card in cards:
        title_tag = card.select_one("h4")
        if not title_tag: continue
        
        title = title_tag.text.strip()
        
        if title in custom_data:
            data = custom_data[title]
            card["data-adv"] = data["adv"]
            card["data-desc"] = data["desc"]
            card["data-time"] = data["time"]
            
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(soup.prettify(formatter="html"))
        
print("Updated specifically detailed descriptions and times for all cards!")
