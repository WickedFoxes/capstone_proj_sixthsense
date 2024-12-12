package com.capstone.sixthsense.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

@Configuration
@EnableMethodSecurity
public class SecurityConfig {
    private final CustomAuthenticationEntryPoint customAuthenticationEntryPoint;
    private final CustomAuthenticationFailureHandler customAuthenticationFailureHandler;
    
    public SecurityConfig(
    		CustomAuthenticationEntryPoint customAuthenticationEntryPoint, 
    		CustomAuthenticationFailureHandler customAuthenticationFailureHandler
    	) {
        this.customAuthenticationEntryPoint = customAuthenticationEntryPoint;
        this.customAuthenticationFailureHandler = customAuthenticationFailureHandler;
    }
    
	@Value("${chrome_ex_path}")
	String chrome_ex_path;
	@Value("${frontend_domain_path}")
	String frontend_domain_path;
	
	
    /* CORS 설정을 위한 새로운 메서드 작성  */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.addAllowedOriginPattern(frontend_domain_path);
        configuration.addAllowedOriginPattern(chrome_ex_path);
//        configuration.addAllowedOrigin("추가 origin 주소");
        configuration.addAllowedMethod("*"); // 모든 HTTP 메소드 허용
        configuration.addAllowedHeader("*"); // 모든 헤더 허용
        configuration.setAllowCredentials(true); // 쿠키 허용
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration); // 모든 경로에 대해 위 설정 적용
        return source;
    }
    
	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
		return http
				.csrf(AbstractHttpConfigurer::disable)
				.cors(httpSecurityCorsConfigurer -> httpSecurityCorsConfigurer
						.configurationSource(corsConfigurationSource())
				)
				.authorizeHttpRequests(request -> request
		        .requestMatchers(
		        		"/", 
		        		"/auth/login", 
		        		"/auth/signup", 
		        		"/auth/logout",
		        		"/image/save/by-key/*",
		        		"/page/list/ready/by-key/*",
		        		"/page/update/by-key/*",
		        		"/item/create/by-page/by-key/*/*",
		        		"/scan/delete/by-page/by-key/*/*",
		        		"/scan/create/by-page/by-item/by-key/*/*/*",		        		
		        		"/schedule/update/by-schedule/by-key/*/*",
		        		"/schedule/list/nextschedule/by-key/*",
		        		"/page/run/by-project/by-key/*/*",
		        		"/test/**"
		        )
		        .permitAll() // Allow these endpoints without authentication
		        .anyRequest().authenticated() // All other requests require authentication
				)
	            .exceptionHandling(exceptionHandling -> exceptionHandling
	                    .authenticationEntryPoint(customAuthenticationEntryPoint) // 인증되지 않은 사용자 처리
	            )
//	            .formLogin(form -> form
//	                    .loginProcessingUrl("/auth/login")     // URL to submit the login form
//	                    .failureHandler(customAuthenticationFailureHandler) // 로그인 실패 처리
//	                    .defaultSuccessUrl("/", true)          // redirect after successful login
//	             )
				.logout((logout) -> logout
			            .logoutUrl("/auth/logout")  // 로그아웃 요청을 처리할 URL
			            .logoutSuccessUrl("/")  // 로그아웃 성공 후 이동할 URL
			            .invalidateHttpSession(true)  // 세션 무효화
			            .clearAuthentication(true)  // 인증 정보 제거
			            .deleteCookies("JSESSIONID") // JSESSIONID 쿠키 삭제
			            .permitAll()  // 모든 사용자에게 로그아웃 접근 허용
	            )
				.sessionManagement(session -> session
		                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)  // 세션 필요 시 생성
		                .maximumSessions(1)  // 동시 세션 1개로 제한
		                .maxSessionsPreventsLogin(true)  // 최대 세션 초과 시 새로운 로그인 차단
				)
				.build();
	}
	
    @Bean
    PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    // AuthenticationManager 빈을 정의합니다.
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }
}