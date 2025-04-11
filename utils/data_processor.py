import pandas as pd
import numpy as np
import re
import logging
from utils.utils import DateUtils, LocationUtils, TextUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnimalDataProcessor:
    """유기동물 데이터 전처리를 담당하는 클래스"""
    
    def __init__(self, df):
        """
        초기화 함수
        
        Parameters:
        df (pandas.DataFrame): 처리할 원본 데이터프레임
        """
        self.df = df.copy()
        
        # 색상 및 패턴 키워드 통합 사전
        self.COLOR_PATTERNS = {
            # 기본 색상
            '검정': ['검정', '검정색', '검은색', '검', '흑색', '흑', '블랙'],
            '흰색': ['흰색', '흰', '백색', '백', '하얀색', '아이보리', '크림색', '크림', '화이트'],
            '갈색': ['갈색', '갈', '연갈색', '연갈', '황갈색', '황토색', '브라운', '밤갈색', '초콜릿색'],
            '노랑': ['황색', '노랑', '노란색', '노랑색', '황', '금색', '옐로우', '누런색'],
            '회색': ['회색', '회', '그레이', '그레이색'],
            
            # 무늬/패턴
            '고등어무늬': ['고등어', '고등어색', '고등어태비'],
            '치즈무늬': ['치즈', '치즈색', '치즈태비'],
            '턱시도무늬': ['턱시도'],
            '태비무늬': ['태비'],
            '호피무늬': ['호피']
        }
        
        # 색상 카테고리 정의
        self.COLOR_TYPES = {
            '단색': ['검정', '흰색', '갈색', '노랑', '회색'],
            '무늬': ['고등어무늬', '치즈무늬', '턱시도무늬', '태비무늬', '호피무늬']
        }
        
        # 장소 유형 매핑
        self.PLACE_TYPE_MAPPING = {
            '공공기관': ['소방서', '구청', '시청', '경찰서', '주민센터', '학교', '대학', '도서관', '우체국', '공공기관', '사무소', '청사', '센터'],
            '상업시설': ['마트', '시장', '상가', '쇼핑', '편의점', '백화점', '매장', '가게', '식당', '카페', '음식점', '마을회관', '슈퍼'],
            '주거지역': ['아파트', '주택', '빌라', '마을', '차', '단지', '동네', '오피스텔', '다세대'],
            '도로변': ['로', '길', '도로', '거리', '대로', '번길', '버스', '버스정류장', '교차로', '사거리', '고가', '다리', '철길', '지하도'],
            '공원': ['공원', '산책로', '광장', '정원', '산', '숲', '강', '하천', '계곡', '저수지', '호수', '유원지', '놀이터'],
            '농촌지역': ['농장', '논', '밭', '과수원', '농지', '축사', '목장', '양식장', '비닐하우스', '창고'],
            '공사장': ['공사장', '건설', '공사', '폐가', '폐건물', '공터', '빈터', '유휴지'],
            '교통시설': ['역', '지하철', '기차', '고속도로', '휴게소', '주차장', '정류소', '환승센터', '공항', '철도'],
            '종교시설': ['교회', '성당', '사찰', '절', '묘지', '납골당', '종교'],
        }
        
        # 시설 특성 매핑
        self.FACILITY_TYPE_MAPPING = {
            '소방서': ['소방서', '119', '구조대', '안전센터'],
            '병원': ['병원', '의원', '보건소', '진료소', '의료', '약국', '동물병원', '의료원'],
            '관공서': ['시청', '구청', '동사무소', '주민센터', '관공서', '군청', '행정', '관리사무소', '공단', '공사'],
            '버스정류장': ['버스', '정류장', '버스정류장', '터미널', '승강장'],
            '교육시설': ['학교', '유치원', '어린이집', '대학교', '학원', '도서관', '연구소', '교육', '훈련원','대학'],
            '복지시설': ['복지관', '경로당', '양로원', '보육원', '쉼터', '보호소', '재활원'],
            '체육시설': ['체육관', '운동장', '구장', '경기장', '스포츠센터', '수영장', '헬스장', '골프장'],
            '공원및녹지': ['공원', '놀이터', '광장', '정원', '산책로', '녹지', '휴식공간'],
            '상업시설': ['상가', '시장', '마트', '슈퍼', '편의점', '매장', '백화점', '쇼핑', '상점'],
            '식음료': ['식당', '카페', '음식점', '레스토랑', '주점', '호프', '분식'],
            '주거시설': ['아파트', '주택', '빌라', '오피스텔', '다세대', '기숙사', '생활관'],
            '산업시설': ['공장', '창고', '물류', '산업', '연구소', '단지'],
            '철도시설': ['역', '기차역', '지하철역', '철도', '전철', '지하철', 'KTX', 'SRT', '광역철도'],
            '터미널': ['터미널', '고속버스', '시외버스', '환승센터', '공항'],
            '기타': [],
        }
        
        # 장소 유형 우선순위 정의
        self.PRIORITY_ORDER = [
            '공공기관', '상업시설', '교육시설', '병원', '종교시설', '복지시설', 
            '공원', '주거지역', '농촌지역', '도로변', '교통시설', '공사장'
        ]
    
    def preprocess_data(self):
        """
        데이터 전처리 실행
        
        Returns:
        pandas.DataFrame: 전처리된 데이터프레임
        """
        logger.info("데이터 전처리 시작")
        
        # 1. 필요 컬럼만 선택
        self._select_necessary_columns()
        
        # 2. 데이터 타입 변환 (날짜 처리)
        self._convert_date_columns()
        
        # 3. 시간 구성요소 추출 (년, 월, 요일, 계절 등)
        self._extract_time_components()
        
        # 4. 동물 종류 및 상태 처리
        self._process_animal_type_and_status()
        
        # 5. 색상 정보 처리
        self._process_color_information()
        
        # 6. 위치 정보 처리
        self._process_location_information()
        
        # 7. 체중 정보 처리
        self._process_weight_information()
        
        # 8. 품종 정보 처리
        self._process_breed_information()
        
        logger.info("데이터 전처리 완료")
        return self.df

    def _select_necessary_columns(self):
        """불필요한 컬럼 제거"""
        try:
            del_col = ['notice_no', 'desertion_no', 'filename', 'popfile', 'charge_nm', 'officetel', 'care_tel']
            columns_to_drop = [col for col in del_col if col in self.df.columns]
            if columns_to_drop:
                self.df = self.df.drop(columns=columns_to_drop)
                logger.info(f"불필요한 컬럼 {len(columns_to_drop)}개 제거 완료")
        except Exception as e:
            logger.error(f"컬럼 제거 중 오류 발생: {e}")
    
    def _convert_date_columns(self):
        """날짜 컬럼 처리"""
        try:
            # DateUtils 클래스에서 제공하는 메서드 활용
            self.df = DateUtils.convert_date_columns(self.df, format='%Y%m%d')
            logger.info("날짜 컬럼 변환 완료")
        except Exception as e:
            logger.error(f"날짜 컬럼 처리 중 오류 발생: {e}")

    def _extract_time_components(self):
        """날짜 컬럼에서 시간 구성요소(년, 월, 요일, 계절) 추출"""
        try:
            # 변환된 날짜 컬럼 찾기
            date_columns = [col for col in self.df.columns if pd.api.types.is_datetime64_any_dtype(self.df[col])]
            
            for date_column in date_columns:
                # DateUtils 클래스에서 제공하는 메서드 활용하여 시간 구성요소 추출
                self.df = DateUtils.extract_time_components(self.df, date_column)
            
            logger.info("시간 구성요소 추출 완료")
        except Exception as e:
            logger.error(f"시간 구성요소 추출 중 오류 발생: {e}")
    
    def _process_animal_type_and_status(self):
        """동물 종류 및 상태 정보 처리"""
        try:
            # 동물 종류 처리
            if 'kind_cd' in self.df.columns:
                self.df['animal_type'] = self.df['kind_cd'].apply(
                    lambda x: '개' if '개' in str(x) else ('고양이' if '고양이' in str(x) else '기타')
                )
                logger.info("동물 종류 처리 완료")
            
            # 동물 상태 처리
            if 'process_state' in self.df.columns:
                self.df['process_state'] = self.df['process_state'].apply(
                    lambda x: x if x == '보호중' else x.replace('종료(', '').replace(')', '')
                )
                self.df['process_cat'] = self.df['process_state'].apply(
                    lambda x: '보호중' if x == '보호중' else '종료'
                )
                logger.info("동물 상태 처리 완료")
            
            # 성별 및 중성화 정보 처리
            if 'sex_cd' in self.df.columns and 'neuter_yn' in self.df.columns:
                self.df = self.process_animal_status(self.df)
                logger.info("성별 및 중성화 정보 처리 완료")
        except Exception as e:
            logger.error(f"동물 종류 및 상태 처리 중 오류 발생: {e}")
    
    def process_animal_status(self, df, sex_col='sex_cd', neuter_col='neuter_yn'):
        """성별 및 중성화 정보 처리 후 컬럼명을 한글로 변경"""
        try:
            # 1. 상태값 계산 (영문 컬럼명 사용)
            conditions = [
                (df[sex_col] == 'M') & (df[neuter_col] == 'Y'),
                (df[sex_col] == 'M') & (df[neuter_col] == 'N'),
                (df[sex_col] == 'F') & (df[neuter_col] == 'Y'),
                (df[sex_col] == 'F') & (df[neuter_col] == 'N'),
                (df[sex_col] == 'Q') | (df[neuter_col] == 'U')
            ]
            choices = [
                '중성화된 수컷', 
                '중성화되지 않은 수컷', 
                '중성화된 암컷', 
                '중성화되지 않은 암컷', 
                '미상'
            ]
            df['animal_status'] = np.select(conditions, choices, default='정보없음')
            
            # 2. 개별 값 한글로 변환
            sex_map = {'M': '수컷', 'F': '암컷', 'Q': '미상'}
            neuter_map = {'Y': '중성화O', 'N': '중성화X', 'U': '미상'}
            
            df['sex_cd'] = df[sex_col].map(sex_map)
            df['neuter_yn'] = df[neuter_col].map(neuter_map)
            
            return df
        except Exception as e:
            logger.error(f"동물 상태 처리 중 오류 발생: {e}")
            return df  # 오류 발생 시 원본 반환
    
    def _process_color_information(self):
        """색상 정보 처리"""
        try:
            if 'color_cd' in self.df.columns:
                # 색상 필터링: ~동, ~구, ~시, ~로 포함 되는 경우 미상으로 처리
                noise_pattern = r'(동|구|시|리|면|부근|길)'
                self.df['color_cd'] = self.df['color_cd'].apply(
                    lambda x: re.sub(f'.*{noise_pattern}.*', '확인필요', x) if isinstance(x, str) and re.search(noise_pattern, x) else x
                )
                
                # 색상 처리 함수 적용
                self.df = self.process_color_column(self.df, 'color_cd')
                logger.info("색상 정보 처리 완료")
        except Exception as e:
            logger.error(f"색상 정보 처리 중 오류 발생: {e}")
    
    def extract_colors_from_text(self, text):
        """텍스트에서 색상 키워드를 추출하여 표준화된 색상명 반환"""
        if pd.isna(text):
            return []
        
        text = str(text).lower()
        found_colors = []
        
        # 여러 구분자로 텍스트 분리
        parts = re.split(r'[,/·\s]+', text)
        parts = [part.strip() for part in parts if part.strip()]
        
        # 각 부분에서 색상 찾기
        for part in parts:
            for color_name, keywords in self.COLOR_PATTERNS.items():
                if any(keyword.lower() in part for keyword in keywords):
                    if color_name not in found_colors:
                        found_colors.append(color_name)
        
        return found_colors
    
    def identify_color_category(self, colors):
        """개선된 색상 카테고리 식별 함수"""
        if not colors:
            return '확인필요'
        
        # 분류를 위한 색상 그룹 분류
        basic_colors = [c for c in colors if c in self.COLOR_TYPES['단색']]
        pattern_colors = [c for c in colors if c in self.COLOR_TYPES['무늬']]
        
        # 무늬가 있는 경우 우선 처리
        if pattern_colors:
            pattern = pattern_colors[0]
            if len(colors) == 1:
                return f'무늬({pattern})'
            else:
                return f'무늬({pattern})+조합'
        
        # 단색인 경우
        if len(basic_colors) == 1:
            return f'단색({basic_colors[0]})'
        
        # 이색 조합
        elif len(basic_colors) == 2:
            return f'이색({"+".join(basic_colors)})'
        
        # 삼색 이상 조합
        elif len(basic_colors) >= 3:
            return f'삼색이상({"+".join(basic_colors[:3])})'
        
        # 기타 케이스
        return f'기타({"+".join(colors[:3]) if colors else ""})'
    
    def process_color_column(self, df, color_column):
        """데이터프레임의 색상 컬럼을 처리하여 새로운 컬럼 추가"""
        # 추출된 색상 목록 컬럼 추가 (리스트 형태로 저장)
        df['color_list_raw'] = df[color_column].apply(self.extract_colors_from_text)
        
        # 색상 카테고리 컬럼 추가 (리스트를 사용)
        df['color_cat'] = df['color_list_raw'].apply(self.identify_color_category)
        
        # 추출된 색상 목록을 /로 구분된 문자열로 변환 (표시용)
        df['color_list'] = df['color_list_raw'].apply(
            lambda colors: '/'.join(colors) if colors else '확인필요'
        )
        
        # 단색/무늬/이색/삼색 등 분류 컬럼 추가
        df['color_type'] = df['color_cat'].apply(
            lambda x: x.split('(')[0] if '(' in x else x
        )
        
        df = df.drop(columns=['color_list_raw'])
        
        return df
    
    
    def get_priority_place_type(self, location_text):
        """우선순위 기반으로 장소 유형 결정"""
        if pd.isna(location_text):
            return "기타"
            
        location_text = str(location_text)
        
        # 일치하는 모든 장소 유형 찾기
        matched_types = []
        for place_type, keywords in self.PLACE_TYPE_MAPPING.items():
            for keyword in keywords:
                if keyword in location_text:
                    matched_types.append(place_type)
                    break
        
        # 우선순위 높은 순으로 반환
        for priority_type in self.PRIORITY_ORDER:
            if priority_type in matched_types:
                return priority_type
        
        # 일치하는 타입이 없으면 기타
        return "기타"
    
    def classify_location(self, location_text):
        """입력 텍스트에서 장소 정보 종합 분류"""
        if pd.isna(location_text):
            return {
                "original_text": "",
                "place_type": "기타",
                "facility_types": ["기타"]
            }
            
        location_text = str(location_text)
        
        # 우선순위에 따라 장소 유형 결정
        place_type = self.get_priority_place_type(location_text)
        
        # 시설 특성 결정 
        facility_types = []
        for facility_type, keywords in self.FACILITY_TYPE_MAPPING.items():
            for keyword in keywords:
                if keyword in location_text:
                    facility_types.append(facility_type)
                    break
        
        result = {
            "original_text": location_text,
            "place_type": place_type,
            "facility_types": facility_types if facility_types else ["기타"]
        }
        return result
    
    
    def classify_locations_in_dataframe(self, df, location_column):
        """
        데이터프레임의 장소 컬럼을 분류하여 장소 유형과 시설 특성 컬럼 추가
        """
        # 장소 유형 추가
        df['place_type'] = df[location_column].apply(
            lambda x: self.get_priority_place_type(str(x)) if pd.notna(x) else '기타'
        )
        # print(df)
        
        # 시설 특성 추가
        df['facility_types'] = df[location_column].apply(
            lambda x: ', '.join(self.classify_location(str(x))['facility_types']) if pd.notna(x) else '기타'
        )
        
        return df
    
    def _process_location_information(self):
        """위치 정보 처리"""
        try:
            # 1. 발견 장소 처리 (happen_place 또는 happenPlace)
            location_column = None
            if 'happen_place' in self.df.columns:
                location_column = 'happen_place'
            
            if location_column:
                # 장소 유형 및 시설 특성 분류 (내부 메서드 활용)
                self.df = self.classify_locations_in_dataframe(self.df, location_column)
                logger.info(f"{location_column} 컬럼에서 장소 유형 및 시설 특성 분류 완료")
            
            # 2. 보호소 주소 처리 (care_addr)
            if 'care_addr' in self.df.columns:
                # utils.py의 LocationUtils 클래스 활용하여 시도, 시군구, 권역 정보 추출
                self.df = LocationUtils.apply_to_dataframe(self.df, 'care_addr')
                logger.info("care_addr 컬럼에서 시도, 시군구, 권역 정보 추출 완료")
                
        except Exception as e:
            logger.error(f"위치 정보 처리 중 오류 발생: {e}")
    
    
    def _process_breed_information(self):
        """품종 정보 처리"""
        try:
            if 'kind_cd' in self.df.columns:
                # utils.py의 TextUtils 클래스 활용
                self.df['breed'] = self.df['kind_cd'].apply(TextUtils.extract_breed)
                logger.info("품종 정보 처리 완료")
        except Exception as e:
            logger.error(f"품종 정보 처리 중 오류 발생: {e}")
    
    def _process_weight_information(self):
        """체중 정보 처리"""
        try:
            if 'weight' in self.df.columns:
                # utils.py의 TextUtils 클래스 활용
                self.df['weight'] = self.df['weight'].apply(TextUtils.extract_weight)
                logger.info("체중 정보 처리 완료")
        except Exception as e:
            logger.error(f"체중 정보 처리 중 오류 발생: {e}")
        
    

    
